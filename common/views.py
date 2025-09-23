from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required

# Create your views here.
def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            if user.role == "HIM":
                return redirect("/him/")
            elif user.role == "NURSE":
                return redirect("/nurse/")
            elif user.role == "DOCTOR":
                return redirect("/doctor/")
            elif user.role == "PHARMACY":
                return redirect("/pharmacy/")
            return redirect('/login')
        else:
            messages.info(request, 'Credetials Invalid')
            return redirect('/login')
    else:
        return render(request, 'common/login.html')

    return render(request, 'common/login.html')


@login_required
def Logout(request):
    auth.logout(request)
    return redirect('/')