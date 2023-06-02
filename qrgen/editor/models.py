from django.db import models

class QrCode(models.Model):
    url = models.CharField(max_length=255)
    image = models.ImageField(upload_to="media/")

