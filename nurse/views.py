from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.db.models import Q
from django.core.paginator import Paginator
from .models import *
from django.contrib import messages

from django.contrib.auth.models import User, auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test

import uuid
# from django.utils.uuid import UUID
from datetime import datetime

import csv
from django.http import HttpResponse

from common.models import Patient, PatientNote, MedicalHistory, VitalSigns, CaseFolder

def is_nurse(user):
    return user.is_authenticated and user.role == "NURSE"

# Create your views here.
# @login_required
# @user_passes_test(is_nurse, login_url="/404")
@login_required
@user_passes_test(is_nurse, login_url="/404")
def NurseDashboard(request):
            
    return render(request, 'nurse/luv_index.html')

@login_required
@user_passes_test(is_nurse, login_url="/404")
def NurseRegAll(request):
    # Get all patients who do not have a MedicalHistory
    patients = Patient.objects.exclude(case_folders__medical_history__isnull=False).distinct()

    context = {
        'patients': patients,
    }

    return render(request, 'nurse/regpatientall.html', context)

@login_required
@user_passes_test(is_nurse, login_url="/404")
def NurseRegEach(request, id):
    patient = Patient.objects.filter(id=id).first()
    # Get the patient or return 404 if not found
    patient = get_object_or_404(Patient, id=id)
    case_folder = get_object_or_404(CaseFolder, patient=patient)

    # Check if the patient has medical history
    has_medical_history = MedicalHistory.objects.filter(case_folder__patient=patient).exists()
    if has_medical_history:
        messages.error(request, "This patient already has a medical history and cannot be registered again.")
        return redirect(reverse('nurse_reg_all'))  # Replace 'dashboard' with your actual dashboard URL name

    if request.method == 'POST':
        # Capture vital signs
        bp = request.POST.get('bp')
        pulse = request.POST.get('pulse')
        weight = request.POST.get('weight')
        height = request.POST.get('height')
        urinealb = request.POST.get('urinealb')
        urinesugar = request.POST.get('urinesugar')

        # # Capture diagnosis and admission details
        # diagnosis = request.POST.get('diagnosis', '').strip()
        # admission_date = request.POST.get('admissionDate')
        # discharge_date = request.POST.get('dischargeDate')

        # Capture medical history (checkboxes)
       
        hypertension = request.POST.get('disease-hypertension', 'off') == 'on'
        measles = request.POST.get('disease-measles', 'off') == 'on'
        chickenpox = request.POST.get('disease-chicken pox', 'off') == 'on'
        tb = request.POST.get('disease-tb', 'off') == 'on'
        diabetes = request.POST.get('disease-diabetes', 'off') == 'on'
        yellowfever = request.POST.get('disease-yellow fever', 'off') == 'on'
        sti = request.POST.get('disease-sti', 'off') == 'on'
        kidneydisease = request.POST.get('disease-kidney disease', 'off') == 'on'
        liverdisease = request.POST.get('disease-liver disease', 'off') == 'on'
        epilepsy = request.POST.get('disease-epilepsy', 'off') == 'on'
        scdisease = request.POST.get('disease-sc disease', 'off') == 'on'
        gdulcer = request.POST.get('disease-gd ulcer', 'off') == 'on'
        rtainjury = request.POST.get('disease-rta injury', 'off') == 'on'
        alcohol = request.POST.get('disease-alcohol or smoking', 'off') == 'on'
        prevops = request.POST.get('disease-previous operation', 'off') == 'on'
        schistosomiasis = request.POST.get('disease-schistosomiasis', 'off') == 'on'
        respiratorydisease = request.POST.get('disease-respiratory disease', 'off') == 'on'
        mentaldisease = request.POST.get('disease-mental disease', 'off') == 'on'
        hiv = request.POST.get('disease-hiv/aids', 'off') == 'on'
        allergies = request.POST.get('disease-allergies', 'off') == 'on'
        
        # Validate required fields
        # required_fields = [bp, pulse, weight, height]
        # if not all(field for field in required_fields):
        #     messages.error(request, "All vital signs and medical history are required.")
        #     return redirect('/nurse/registration/all/')
        
        vitals_instance, created = VitalSigns.objects.update_or_create(case_folder=case_folder,
        blood_pressure=bp, pulse=pulse, weight=weight, height=height,
        urine_albumin=urinealb, urine_sugar=urinesugar, recorded_by=request.user)

        

        # Create or update MedicalHistory
        medical_history_instance, created = MedicalHistory.objects.update_or_create(
            case_folder=case_folder,
            recorded_by=request.user,
            defaults={
                'hypertension': hypertension,
                'measles': measles,
                'chicken_pox': chickenpox,
                'tb': tb,
                'diabetes': diabetes,
                'yellow_fever': yellowfever,
                'sti': sti,
                'kidney_disease': kidneydisease,
                'liver_disease': liverdisease,
                'epilepsy': epilepsy,
                'sc_disease': scdisease,
                'gd_ulcer': gdulcer,
                'rta_injury': rtainjury,
                'alcohol_smoking': alcohol,
                'previous_ops': prevops,
                'schistosomiasis': schistosomiasis,
                'respiratory_disease': respiratorydisease,
                'mental_disease': mentaldisease,
                'hiv': hiv,
                'allergies': allergies,
                'recorded_by': request.user,
            }
        )

        
        messages.success(request, "Patient vitals and medical history saved successfully.")
        # return redirect(reverse('nurse_reg_all', kwargs={'id': patient.id}))
        return redirect('/nurse/registration/all/')

        
    

    context = {
        'patient': patient,
        'diseases': ['hypertension', 'measles', 'chicken pox', 'tb', 'diabetes',
        'yellow fever', 'sti', 'kidney disease', 'liver disease', 'epilepsy', 'sc disease',
        'gd ulcer', 'rta injury', 'alcohol or smoking', 'previous operation', 'schistosomiasis',
        'respiratory disease', 'mental disease', 'hiv/aids', 'allergies']
    }
            
    return render(request, 'nurse/luv_patientregistration.html', context)

def NurseAttendPatientsList(request):
    patients = Patient.objects.all()

    if request.method == 'POST':
        search = request.POST.get('searchTerm', '').lower()

        if search:
            patients = patients.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(id_no__icontains=search)
            ).distinct()
        
    
    context = {
        'patients': patients,
    }
    
    return render(request, 'nurse/attendpatientlist.html', context)

def NurseAttendPatientsEach(request, id):
            
    return render(request, 'nurse/attendpatients.html')

def NurseInPatientList(request):
            
    return render(request, 'nurse/inpatientcarelist.html')

def NurseInPatient(request, id):
            
    return render(request, 'nurse/luv_inpatientcare.html')

def Reports(request):
            
    return render(request, 'nurse/luv_reports.html')