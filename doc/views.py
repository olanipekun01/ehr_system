from django.shortcuts import render

# Create your views here.
def DoctorDashboard(request):
            
    return render(request, 'doctor/dashboard.html')

def DoctorConsultations(request):
            
    return render(request, 'doctor/consultations.html')