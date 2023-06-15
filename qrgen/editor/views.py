from qrgen.settings import MEDIA_URL, BASE_DIR
from .generate_qr import *
from userpages.models import *
# import mimetypes
from pathlib import *
from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.http import FileResponse
from django.contrib.auth import authenticate
from django.core.files.storage import FileSystemStorage
import os

from .models import QrCode, UserImage, LittleImage
import PIL
from PIL import Image, ImageDraw

def form_check(form):
    if form == "SquareModuleDrawer()":
        form = SquareModuleDrawer()
    if form == "CircleModuleDrawer()":
        form = CircleModuleDrawer() 
    if form == "GappedSquareModuleDrawer()":    
        form = GappedSquareModuleDrawer()
    if form == "RoundedModuleDrawer()":
        form = RoundedModuleDrawer()
    if form == "VerticalBarsDrawer()":
        form = VerticalBarsDrawer()
    if form == "HorizontalBarsDrawer()":
        form = HorizontalBarsDrawer() 
    return form      

def gradiant_check(gradiant, c1, c2, c3, image = None):
    if gradiant == "SolidFillColorMask()":
        gradiant = SolidFillColorMask(c1,c2)
    if gradiant == "RadialGradiantColorMask()":
        gradiant = RadialGradiantColorMask(c1,c2,c3)
    if gradiant == "SquareGradiantColorMask()":
        gradiant = SquareGradiantColorMask(c1,c2,c3)    
    if gradiant == "VerticalGradiantColorMask()":
        gradiant = VerticalGradiantColorMask(c1,c2,c3)
    if gradiant == "HorizontalGradiantColorMask()":
        gradiant = HorizontalGradiantColorMask(c1,c2,c3)
    if gradiant == "ImageColorMask()":
        gradiant = ImageColorMask(color_mask_image=image)
    return gradiant    


def hex_to_rgb(hex):
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

def show_editor(request):
    context = {
        "url":None
    }

    if request.method == "GET" and not request.user.is_authenticated:
        return redirect("login")

    if UserMod.objects.get(user=User.objects.get(username=request.user)).plan.plantype == "Free":
        return redirect("main")
        
    if request.method == "POST":    

        qr_var = request.POST
        back = qr_var["back_color"][1:]#tip uberau hashteg
        first = qr_var["first_color"][1:]
        second = qr_var["second_color"][1:]
        block_form = qr_var["block_form"]
        gradiant_form = qr_var["gradiant_form"]
        url = qr_var['qr_url']
        extension = qr_var["extention"]

        block_form = form_check(block_form)
        name = request.user
        user = UserMod.objects.get(user=User.objects.get(username=name))

        
        b1 = hex_to_rgb(back)
        f1 = hex_to_rgb(first)
        s1 = hex_to_rgb(second)

        # print(qr_var)

        if "load_file_little" in request.FILES:
            little_qr_img = request.FILES["load_file_little"]
            little_img = LittleImage(image_little = little_qr_img)
            little_img.save(little_qr_img)
            final_little_img = MEDIA_URL+f"media/{little_qr_img}"
        else:
            final_little_img = None

        if "load_file" in request.FILES:
            in_qr_img = request.FILES["load_file"]
            bg_img = UserImage(image_bg=in_qr_img)
            bg_img.save(in_qr_img)
            final_img = Image.open(MEDIA_URL+f"media/{in_qr_img}")
            # print(in_qr_img)
            gradiant_form = gradiant_check(gradiant_form,b1,f1,s1,final_img) 

        else:
            gradiant_form = gradiant_check(gradiant_form,b1,f1,s1)     

        if not os.path.exists(MEDIA_URL+f"{name}"):
            os.mkdir(MEDIA_URL+f"{name}")

        final_qr = QrCode.addQr(user = user, url= url, qrcode_path = None)
        new_qr = make_qr(qr_data = f"http://localhost:8000/redirect/{final_qr.pk}", image_center=final_little_img, black_form=block_form, gradient = gradiant_form)
        qr_path = f"{name}/generated_qr{len(QrCode.objects.filter(user = UserMod.objects.get(user = User.objects.get(username = name))))+1}.{extension}"
        new_qr.save(MEDIA_URL+qr_path)
        final_qr.image = qr_path
        # if final_qr in 
        final_qr.save()

        if "load_file" in request.FILES:
            bg_img.delete()
        
        if "load_file_little" in request.FILES:
            little_img.delete()
        user.qr_amount += 1
        user.save()
        context["url"] = final_qr
        
    respones = render(request, "editor/editor.html", context)
    return respones

