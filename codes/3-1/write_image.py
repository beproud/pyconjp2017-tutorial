# write_image.py

from PIL import Image


with Image.open('./2017.png', 'r') as im:
    im.save('./2017.jpg', 'JPEG')
