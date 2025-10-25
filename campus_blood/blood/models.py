from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Donor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    blood_group = models.CharField(max_length=5)
    phone = models.CharField(max_length=15)
    department = models.CharField(max_length=100)
    available = models.BooleanField(default=True)
    last_donation_date = models.DateField(null=True, blank=True)
    donation_count = models.IntegerField(default=0)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.blood_group}"

class Request(models.Model):
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE, related_name='requests')
    requester = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField(blank=True)
    date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, default="Pending")  # Pending / Approved / Rejected

    def __str__(self):
        return f"{self.requester.username} → {self.donor.user.username} ({self.status})"
