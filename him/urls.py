from django.urls import path
from . import views

app_name = "him"

urlpatterns = [
    path('/', views.RegisterPatients, name='register'),
]