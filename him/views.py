from django.shortcuts import render, redirect, get_object_or_404
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

def is_him(user):
    return user.is_authenticated and user.role == "HIM"

# Create your views here.
@login_required
@user_passes_test(is_him, login_url="/404")
def HimDashboard(request):
            
    return render(request, 'him/dashboard.html')


@login_required
@user_passes_test(is_him, login_url="/404")
def RegisterPatients(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        dob = request.POST["dob"]
        gender = request.POST["gender"]
        status = request.POST["status"]
        id_no = request.POST.get("id_no", "")
        xray_no = request.POST.get("xray_no", "")
        phone = request.POST.get("phone", "")
        email = request.POST.get("email", "")
        address = request.POST.get("address", "")
        religion = request.POST.get("religion", "")
        state_of_origin = request.POST.get("state_of_origin", "")
        Tribe = request.POST.get("Tribe", "")
        casefolderNo = request.POST.get("casefolderNo", "")

        patient = Patient.objects.filter(Q(id_no=id_no) | Q(email=email))

        if patient.exists():   # <-- better than just `if patient:`
            messages.error(request, "Patient already exists!")
            return redirect("/him/patients/new/")

        patient = Patient.objects.create(
            first_name=first_name, last_name=last_name, dob=dob, gender=gender,
            id_no=id_no, status=status, address=address, phone=phone, email=email,
            xray_no=xray_no, religion=religion, state_of_origin=state_of_origin,
            Tribe=Tribe, created_by=request.user,
        )

        patient.save()

        casefolder = CaseFolder.objects.create(
            patient = patient,
            folder_number = casefolderNo,
            created_by = request.user,
        )
        casefolder.save()
        messages.success(request, "Patient Information Saved!")
        redirect("/him/dashboard/")
        
    return render(request, 'him/register.html')

@login_required
@user_passes_test(is_him, login_url="/404")
def PatientList(request):
    patients = Patient.objects.all()

    context = {
        "patients": patients
    }
            
    return render(request, 'him/patient_list.html', context)

@login_required
@user_passes_test(is_him, login_url="/404")
def EachPatient(request, id):
    patient = get_object_or_404(Patient, id=id)
    casefolder = CaseFolder.objects.filter(patient=patient).first()
    # if casefolder:
    #     # Get the medical history for this specific case folder
    #     medhistory = get_object_or_404(MedicalHistory, case_folder=casefolder)
    # else:
    #     medhistory = None

    try:
        casefolder = CaseFolder.objects.filter(patient=patient).first()  # Adjust if the relation name differs
        if not casefolder:
            messages.error(request, "No case folder found for this patient.")
            return redirect('/him/patients/list/')  # Redirect to a list view or home
        medhistory = MedicalHistory.objects.filter(case_folder=casefolder).first()
        notes = PatientNote.objects.filter(case_folder=casefolder)
        vitals = VitalSigns.objects.filter(case_folder=casefolder)
    except MedicalHistory.DoesNotExist:
        messages.error(request, "No medical history found for this patient.")
        medhist = None  # Or create a default instance if needed
    except notes.DoesNotExist:
        messages.error(request, "No notes found for this patient.")
        notes = None  # Or create a default instance if needed
    except vitals.DoesNotExist:
        messages.error(request, "No vitals found for this patient.")
        vitals = None  # Or create a default instance if needed
    
    # notes = PatientNote.objects.filter(case_folder=casefolder)
    # medhistory = MedicalHistory.objects.filter(case_folder=casefolder).first()
    # vitals = VitalSigns.objects.filter(case_folder=casefolder)

    context = {
        "patient": patient,
        "casefolder": casefolder,
        "notes": notes,
        "medhist": medhistory,
        "vitals": vitals,
    }

    return render(request, 'him/each_patient.html', context)

@login_required
@user_passes_test(is_him, login_url="/404")
def EditPatientInfo(request, id):
    patient = get_object_or_404(Patient, id=id)
    casefolder = CaseFolder.objects.filter(patient=patient).first()
    # if casefolder:
    #     # Get the medical history for this specific case folder
    #     medhistory = get_object_or_404(MedicalHistory, case_folder=casefolder)
    # else:
    #     medhistory = None
    
    # notes = PatientNote.objects.filter(case_folder=casefolder)
    # medhistory = MedicalHistory.objects.filter(case_folder=casefolder)
    # vitals = VitalSigns.objects.filter(case_folder=casefolder)
    if request.method == "POST":

        patient = get_object_or_404(Patient, id=id)

        if not patient:
            messages.error(request, "Patient doesn't exist!")
            return redirect("/him/patients/new/")

        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        dob = request.POST["dob"]
        gender = request.POST["gender"]
        status = request.POST["status"]
        id_no = request.POST.get("id_no", "")
        xray_no = request.POST.get("xray_no", "")
        phone = request.POST.get("phone", "")
        email = request.POST.get("email", "")
        address = request.POST.get("address", "")
        religion = request.POST.get("religion", "")
        state_of_origin = request.POST.get("state_of_origin", "")
        Tribe = request.POST.get("Tribe", "")
        casefolderNo = request.POST.get("folderNo", "")

        patient.first_name=first_name
        patient.last_name=last_name
        patient.dob=dob
        patient.gender=gender
        patient.id_no=id_no
        patient.status=status
        patient.address=address
        patient.phone=phone
        patient.email=email
        patient.xray_no=xray_no
        patient.religion=religion
        patient.state_of_origin=state_of_origin
        patient.Tribe=Tribe

        patient.save()

        casefolder = CaseFolder.objects.filter(patient=patient).first()
        
        casefolder.folder_number = casefolderNo
        casefolder.save()

        messages.success(request, "Patient Information Updated!")
        return redirect(f'/him/patient/each/{id}/')


    context = {
        "patient": patient,
        "casefolder": casefolder,
        "id": id,
    }


    return render(request, 'him/edit_patient_info.html', context)
