from django.urls import path
from . import views

app_name = "him"

urlpatterns = [
    path('/dashboard/', views.HimDashboard, name="him_dashboard"),
    path('/patients/new/', views.RegisterPatients, name='register'),
    path('/patients/list/', views.PatientList, name='patient_list'),
    path('/patient/each/<uuid:id>/', views.EachPatient, name='each_patient'),
    path('/patient/edit/<uuid:id>/', views.EditPatientInfo, name='edit_patient_info'),
]