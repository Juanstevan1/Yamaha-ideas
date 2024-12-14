from django.contrib.auth.models import User
from django.db import models

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    roles = models.ManyToManyField(Role, related_name="profiles", blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {', '.join(role.name for role in self.roles.all()) or 'No Roles'}"

    @property
    def is_employee(self):
        return self.roles.filter(name="Empleado").exists()

    @property
    def is_coordinator(self):
        return self.roles.filter(name="Coordinador").exists()

    @property
    def is_committee_member(self):
        return self.roles.filter(name="MiembrodelComite").exists()

    @property
    def is_sponsor(self):
        return self.roles.filter(name="Sponsor").exists()
