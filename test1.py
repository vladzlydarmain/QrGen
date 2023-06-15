import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import *
from qrcode.image.styles.colormasks import *

import PIL
from PIL import Image, ImageDraw

# -----------------------------------------------IMPORTANT-----------------------------------------------
def style_inner_eyes(img):
  img_size = img.size[0]
  eye_size = 70 #default
  quiet_zone = 40 #default
  mask = Image.new('L', img.size, 0)
  draw = ImageDraw.Draw(mask)
  draw.rectangle((60, 60, 90, 90), fill=255) #top left eye
  draw.rectangle((img_size-90, 60, img_size-60, 90), fill=255) #top right eye
  draw.rectangle((60, img_size-90, 90, img_size-60), fill=255) #bottom left eye
  return mask

def style_outer_eyes(img):
  img_size = img.size[0]
  eye_size = 70 #default
  quiet_zone = 40 #default
  mask = Image.new('L', img.size, 0)
  draw = ImageDraw.Draw(mask)
  draw.rectangle((40, 40, 110, 110), fill=255) #top left eye
  draw.rectangle((img_size-110, 40, img_size-40, 110), fill=255) #top right eye
  draw.rectangle((40, img_size-110, 110, img_size-40), fill=255) #bottom left eye
  draw.rectangle((60, 60, 90, 90), fill=0) #top left eye
  draw.rectangle((img_size-90, 60, img_size-60, 90), fill=0) #top right eye
  draw.rectangle((60, img_size-90, 90, img_size-60), fill=0) #bottom left eye  
  return mask


def make_qr(qr_data, bor_len=2, vers= 1, image_center = None, black_form = SquareModuleDrawer(), gradient = SolidFillColorMask((255, 255, 255),(0,0,0))):
  if image_center == None:
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, version=vers, box_size=20, border= bor_len)
    qr.add_data(qr_data)
    img = qr.make_image(image_factory=StyledPilImage, module_drawer=black_form, color_mask=gradient)  
    return img
  else:
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, version=vers, box_size=20, border= bor_len)
    qr.add_data(qr_data)
    img = qr.make_image(image_factory=StyledPilImage, module_drawer=black_form, color_mask=gradient, embeded_image_path=image_center)  
    return img

def create_inner_eyes(eye_drawer = SquareModuleDrawer(), color_mask = SolidFillColorMask((255, 255, 255),(0,0,0)),color = (0,0,0)):
  qr_inner_eyes_img = qr.make_image(image_factory=StyledPilImage,
                            eye_drawer=RoundedModuleDrawer(radius_ratio=1.2),
                            color_mask=SolidFillColorMask(front_color=color))
  return qr_inner_eyes_img

def create_outer_eyes(eye_drawer = SquareModuleDrawer(), color_mask = SolidFillColorMask((255, 255, 255),(0,0,0)),color = (0, 0, 0)):
  qr_outer_eyes_img = qr.make_image(image_factory=StyledPilImage,
                            eye_drawer=VerticalBarsDrawer(),
                            color_mask=SolidFillColorMask(front_color=color)) 
  return qr_outer_eyes_img 
# -----------------------------------------------IMPORTANT-----------------------------------------------

if not hasattr(PIL.Image, 'Resampling'):
  PIL.Image.Resampling = PIL.Image

qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)

qr.add_data('http://www.medium.com')

qr_inner_eyes_img = qr.make_image(image_factory=StyledPilImage,
                            eye_drawer=GappedSquareModuleDrawer(),
                            color_mask=SolidFillColorMask(front_color=(63, 42, 86)))

# qr_inner_eyes_img = make_qr(

# )                            

qr_outer_eyes_img = qr.make_image(image_factory=StyledPilImage,
                            eye_drawer=VerticalBarsDrawer(),
                            color_mask=SolidFillColorMask(front_color=(0, 128, 0)))                            


# qr_img = make_qr("")
qr_img = qr.make_image(image_factory=StyledPilImage,
                       module_drawer=SquareModuleDrawer())

# qr_img = make_qr(qr_data="Utochka: krya krya", 
#                  black_form = RoundedModuleDrawer(), #форма кубиков
#                  gradient = VerticalGradiantColorMask((255,255,255), (30,30,30), (90,90,30))
#                 )

# qr_img.save('userqr9090.png')

# -----------------------------------------------IMPORTANT-----------------------------------------------
inner_eye_mask = style_inner_eyes(qr_img)
outer_eye_mask = style_outer_eyes(qr_img)
intermediate_img = Image.composite(qr_inner_eyes_img, qr_img, inner_eye_mask)
final_image = Image.composite(qr_outer_eyes_img, intermediate_img, outer_eye_mask)
# -----------------------------------------------IMPORTANT-----------------------------------------------
final_image.save('final_imageeeeeeeeeeeeee.png')


qr_1 = qr.make_image(image_factory=StyledPilImage,
                       module_drawer=SquareModuleDrawer(),
                       eye_drawer=VerticalBarsDrawer())
qr_1.save('userqr9090.png')                      