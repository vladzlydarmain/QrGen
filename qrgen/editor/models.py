from django.db import models
from userpages.models import UserMod

class UserImage(models.Model):
    image_bg = models.ImageField(upload_to="media/")

class LittleImage(models.Model):
    image_little = models.ImageField(upload_to="media/")

class QrCode(models.Model):
    url = models.CharField(max_length=255)
    image = models.ImageField(upload_to="media/")
    user_img = models.ForeignKey(UserImage, on_delete=models.CASCADE)
    little_user_img = models.ForeignKey(LittleImage, on_delete=models.CASCADE)
    user = models.ForeignKey(UserMod, on_delete=models.CASCADE, default=0)
    def addQr(qrcode_path, user,url,user_img=UserImage.objects.get(pk = 1),little_user_img=LittleImage.objects.get(pk = 1)):
        # if user_img != 0:
        #     qr = QrCode.objects.create(user=user,image=qrcode_path,url = url, user_img = user_img)
        # else:
        qr = QrCode.objects.create(user=user,image=qrcode_path,url = url,user_img=user_img,little_user_img=little_user_img)    
        return  qr
