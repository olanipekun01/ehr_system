from django.urls import path
from . import views

app_name = "nurse"

urlpatterns = [
    path('/dashboard/', views.NurseDashboard, name="nurse_dashboard"),
    path('/registration/all/', views.NurseRegAll, name='nurse_reg_all'),
    path('/registration/each/<str:id>/', views.NurseRegEach, name='nurse_reg_each'),
    path('/attend/patients/list/', views.NurseAttendPatientsList, name='nurse_atend_patient_list'),
    path('/attend/patients/each/<str:id>/', views.NurseAttendPatientsEach, name='nurse_atend_patient'),
    path('/inpatient/list/', views.NurseInPatientList, name='inpatient_list'),
    path('/inpatient/each/<str:id>/', views.NurseInPatient, name='inpatient_each'),
    path('/reports/', views.Reports, name='nurse_reports'),
]