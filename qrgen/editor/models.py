from django.db import models
from userpages.models import UserMod

class QrCode(models.Model):
    url = models.CharField(max_length=255)
    image = models.ImageField(upload_to="media/")
    user_img = None
    user = models.ForeignKey(UserMod, on_delete=models.CASCADE, default=-1)
    def addUser_img(img):
        user_img = models.ImageField(upload_to="media/")
    def addQr(qrcode_path, user,url):
        qr = QrCode.objects.create(user=user,image=qrcode_path,url = url)
        return  qr

