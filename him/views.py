from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from .models import *
from django.contrib import messages

from django.contrib.auth.models import User, auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test

import uuid
from datetime import datetime

import csv
from django.http import HttpResponse

from common.models import Patient

def is_him(user):
    return user.is_authenticated and user.role == "HIM"

# Create your views here.
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

        patient = Patient.objects.filter(Q(id_no=id_no) | Q(email=email))

        if patient.exists():   # <-- better than just `if patient:`
            messages.error(request, "Patient already exists!")
            return redirect("/him/")

        patient = Patient.objects.create(
            first_name=first_name, last_name=last_name, dob=dob, gender=gender,
            id_no=id_no, status=status, address=address, phone=phone, email=email,
            xray_no=xray_no, religion=religion, state_of_origin=state_of_origin,
            Tribe=Tribe, created_by=request.user,
        )

        patient.save()
        messages.success(request, "Patient Information Saved!")
        redirect("/him/")
        
    return render(request, 'him/register.html')

