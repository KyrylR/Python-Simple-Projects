from PIL import Image, ImageFilter

img = Image.open('./images/pikachu.jpg')
filtered_img = img.filter(ImageFilter.BLUR)
filtered_img.save("blur.png", 'png')

# print(img.format)  # JPEG
# print(img.size)  # (640, 640)
# print(img.mode)  # RGB
# print(dir(img))
