import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import *
from qrcode.image.styles.colormasks import *

import PIL
from PIL import Image, ImageDraw

# cool_img = Image.open("231.jpg")
# size = (300,300)
# cool_img = cool_img.resize(size)
# cool_img.save("test.jpg")

def make_qr(qr_data, bor_len=2, vers= 1, image = None, black_form = SquareModuleDrawer(), gradient = SolidFillColorMask((255, 255, 255),(0,0,0))):
  if image == None:
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, version=vers, box_size=20, border= bor_len)
    qr.add_data(qr_data)
    img = qr.make_image(image_factory=StyledPilImage, module_drawer=black_form, color_mask=gradient)  
    return img
  else:
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, version=vers, box_size=20, border= bor_len)
    qr.add_data(qr_data)
    img = qr.make_image(image_factory=StyledPilImage, module_drawer=black_form, color_mask=gradient, embeded_image_path=image)  
    return img






# byaka nize








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


if not hasattr(PIL.Image, 'Resampling'):
  PIL.Image.Resampling = PIL.Image
# Now PIL.Image.Resampling.BICUBIC is always recognized.


qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)

qr.add_data('http://www.medium.com')

qr_inner_eyes_img = qr.make_image(image_factory=StyledPilImage,
                            eye_drawer=RoundedModuleDrawer(radius_ratio=1.2),
                            color_mask=SolidFillColorMask(back_color=(255, 255, 255), front_color=(63, 42, 86)))

qr_outer_eyes_img = qr.make_image(image_factory=StyledPilImage,
                            eye_drawer=VerticalBarsDrawer(),
                            color_mask=SolidFillColorMask(front_color=(255, 128, 0)))                            

qr_img = qr.make_image(image_factory=StyledPilImage,
                       module_drawer=SquareModuleDrawer())

inner_eye_mask = style_inner_eyes(qr_img)
outer_eye_mask = style_outer_eyes(qr_img)
intermediate_img = Image.composite(qr_inner_eyes_img, qr_img, inner_eye_mask)
final_image = Image.composite(qr_outer_eyes_img, intermediate_img, outer_eye_mask)
final_image.save('final_image.png')
# cool_qr = make_qr("Utochka: krya krya", #инфа
#                   2,#растояние от бордера
#                   3,#версия
#                   "test.jpg",#закоменть и фотки не будет
#                   RoundedModuleDrawer(), #форма кубиков
#                   RadialGradiantColorMask(,"#CC4700",'002766')
#                   )#  #градиент, если убрать будет обычный

# cool_qr.save('userqr.png')

