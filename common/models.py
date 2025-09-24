from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
import uuid
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES = [
        ('HIM', 'Health Information Management Officer'),
        ('NURSE', 'Nurse'),
        ('DOCTOR', 'Doctor'),
        ('PHARMACY', 'Pharmacy')
    ]
    username = models.CharField(max_length=100, unique=True, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True, db_index=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15, blank=True)
    is_authorized = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def set_password(self, raw_password):
        """Hash and set the password."""
        self.password = make_password(raw_password)
        
    def check_password(self, raw_password):
        """Check the password against the stored hashed password."""
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.username} ({self.role})"

class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female')
    ]

    RELIGION_CHOICES = [
        ('CHRISTIAN', 'Christianity'),
        ('MUSLIM', 'Muslim'),
        ('OTHER', 'Other'),
    ]

    STATUS_CHOICES = [
        ('STUDENT', 'Student'),
        ('STAFF', 'Staff'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    id_no = models.CharField(max_length=15)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=1)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    xray_no = models.CharField(max_length=15)
    religion = models.CharField(max_length=25, choices=RELIGION_CHOICES)
    state_of_origin = models.CharField(max_length=50)
    Tribe = models.CharField(max_length=60)
    # last_visitation_date
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_patients')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class CaseFolder(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='case_folders')
    folder_number = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_case_folders')
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Case Folder {self.folder_number} - {self.patient}"

class MedicalHistory(models.Model):
    case_folder = models.OneToOneField(CaseFolder, on_delete=models.CASCADE, related_name='medical_history')
    hypertension = models.BooleanField(default=False)
    measles = models.BooleanField(default=False)
    chicken_pox = models.BooleanField(default=False)
    tb = models.BooleanField(default=False)
    diabetes = models.BooleanField(default=False)
    yellow_fever = models.BooleanField(default=False)
    sti = models.BooleanField(default=False)
    kidney_disease = models.BooleanField(default=False)
    liver_disease = models.BooleanField(default=False)
    epilepsy = models.BooleanField(default=False)
    sc_disease = models.BooleanField(default=False)
    gd_ulcer = models.BooleanField(default=False)
    rta_injury = models.BooleanField(default=False)
    alcohol_smoking = models.BooleanField(default=False)
    previous_ops = models.BooleanField(default=False)
    schistosomiasis = models.BooleanField(default=False)
    respiratory_disease = models.BooleanField(default=False)
    mental_disease = models.BooleanField(default=False)
    hiv = models.BooleanField(default=False)
    allergies = models.BooleanField(default=False)
    recorded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recorded_medicalhistory')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Medical History - {self.case_folder.patient}"

class DiagnosisAdmission(models.Model):
    case_folder = models.ForeignKey(CaseFolder, on_delete=models.CASCADE, related_name='diagnoses')
    date = models.DateTimeField()
    diagnosis = models.TextField()
    date_of_admission = models.DateTimeField()
    date_of_discharge = models.DateTimeField(blank=True, null=True)
    recorded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recorded_diagnoses')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_diagnoses')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Diagnosis - {self.case_folder.patient} - {self.date.strftime('%Y-%m-%d')}"

class VitalSigns(models.Model):
    case_folder = models.ForeignKey(CaseFolder, on_delete=models.CASCADE, related_name='vital_signs')
    blood_pressure = models.CharField(max_length=20)  # e.g., "120/80"
    pulse = models.CharField(max_length=10)
    weight = models.CharField(max_length=10)
    height = models.CharField(max_length=10)
    urine_albumin = models.CharField(max_length=20)
    urine_sugar = models.CharField(max_length=20)
    recorded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recorded_vitals')
    recorded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-recorded_at']
    
    def __str__(self):
        return f"Vitals - {self.case_folder.patient} - {self.recorded_at.strftime('%Y-%m-%d')}"

class PatientNote(models.Model):
    USER_TYPE_CHOICES = [
        ('DOCTOR', 'Doctor'),
        ('NURSE', 'Nurse'),
    ]
    
    case_folder = models.ForeignKey(CaseFolder, on_delete=models.CASCADE, related_name='notes')
    surname = models.CharField(max_length=100)
    other_names = models.CharField(max_length=200)
    date = models.DateTimeField()
    notes = models.TextField()
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    recorded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recorded_notes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Note - {self.case_folder.patient} - {self.date.strftime('%Y-%m-%d')}"