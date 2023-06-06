from django.db import models
from django.contrib.auth.models import User
from editor.models import *

# Create your models here.
    
class Plan(models.Model):
    price = models.FloatField()
    plantype = models.CharField(max_length=255)
    qrcode_amount = models.IntegerField()
    scans = models.IntegerField()

class UserMod(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete = models.CASCADE)
    next_payment = None
    qr_scans = 0
    qr_codes_list = [0]
    def addQrCode(url,img):
        qr = QrCode.objects.create(url=url,image = img)
        models.ForeignKey(qr, on_delete = models.CASCADE)
        UserMod.qr_codes_list.append(qr)
        return qr
    