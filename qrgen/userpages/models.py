from django.db import models
from django.contrib.auth.models import User
from editor.models import *

# Create your models here.
    
class Plan(models.Model):
    price = models.CharField(max_length=255)
    plantype = models.CharField(max_length=255)
    qrcode_amount = models.IntegerField()
    scans = models.IntegerField()

class UserMod(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete = models.CASCADE)
    qr_codes = models.ForeignKey(QrCode, on_delete = models.CASCADE)