import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import *
from qrcode.image.styles.colormasks import *

import PIL
from PIL import Image, ImageDraw

cool_img = Image.open("пустота.png")
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


cool_qr = make_qr(qr_data="Utochka: krya krya", #инфа
                  bor_len=2,#растояние от бордера
                  vers= 3,#версия
                  image = "231.jpg",#закоменть и фотки не будет
                  black_form = RoundedModuleDrawer(), #форма кубиков
                  gradient = ImageColorMask(color_mask_image=cool_img)
                  )#  #градиент, если убрать будет обычный

cool_qr.save('userqr.png')
