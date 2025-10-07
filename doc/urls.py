from django.urls import path
from . import views

app_name = "doc"

urlpatterns = [
    path('/dashboard/', views.DoctorDashboard, name="doctor_dashboard"),
    path('/consultations/', views.DoctorConsultations, name='doctor_consultations'),
    # path('/patients/inpatient/', views.NurseInPatient, name='nurse_in_patient'),
    # path('/patient/each/<uuid:id>/', views.EachPatient, name='each_patient'),
    # path('/patient/edit/<uuid:id>/', views.EditPatientInfo, name='edit_patient_info'),
]