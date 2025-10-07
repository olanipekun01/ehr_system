from django.urls import path
from . import views

app_name = "nurse"

urlpatterns = [
    path('/dashboard/', views.NurseDashboard, name="nurse_dashboard"),
    path('/registration/all/', views.NurseRegAll, name='nurse_reg_all'),
    path('/registration/each/<str:id>/', views.NurseRegEach, name='nurse_reg_each'),
    path('/attend/patients/each/', views.NurseAttendPatientsEach, name='nurse_atend_patient'),
    # path('/inpatient/', views.EachPatient, name='each_patient'),
    # path('/reports/', views.EditPatientInfo, name='edit_patient_info'),
]