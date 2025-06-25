from django.db import models
from store.models.location import Location
from django.utils import timezone

class Users(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, default=None, related_name='users')
    xrai_id = models.CharField(max_length=100, default = '0')
    patient_id = models.CharField(max_length=100, default='0')
    patient_name = models.CharField(max_length=100, null=True)
    age = models.IntegerField(null=True, default=None, blank=True)
    gender = models.CharField(max_length=15, null=True)
    phone = models.CharField(max_length=10, null=True, default=None, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    date_field = models.DateField(default=timezone.now)
    current_time = models.DateTimeField(auto_now_add=True)

    registration = models.BooleanField(default=False)
    xray = models.BooleanField(default=False)
    ecg = models.BooleanField(default=False)
    pft = models.BooleanField(default=False)
    audiometry = models.BooleanField(default=False)
    optometry = models.BooleanField(default=False)
    sputum = models.BooleanField(default=False)
    vitals = models.BooleanField(default=False)
    pathology = models.BooleanField(default=False)
    drconsultation = models.BooleanField(default=False)

    def __str__(self):
        return str(self.patient_name)
    

    # 🔽 Add these new fields
    registration_disabled = models.BooleanField(default=False)
    xray_disabled = models.BooleanField(default=False)
    ecg_disabled = models.BooleanField(default=False)
    pft_disabled = models.BooleanField(default=False)
    audiometry_disabled = models.BooleanField(default=False)
    optometry_disabled = models.BooleanField(default=False)
    sputum_disabled = models.BooleanField(default=False)
    vitals_disabled = models.BooleanField(default=False)
    pathology_disabled = models.BooleanField(default=False)
    drconsultation_disabled = models.BooleanField(default=False)