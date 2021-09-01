import sys
import os
from PIL import Image

# grab the first and second argument
image_folder = sys.argv[1]
output_folder = sys.argv[2]

# check if new folder exists, if not create
if not os.path.exists(f'./{output_folder}'):
    os.mkdir(output_folder)
    print(f'Directory {output_folder} created')
else:
    print(f'Directory {output_folder} already exists')


# loop through images,
# convert images to png
# save to the new folder
for filename in os.listdir(image_folder):
    img = Image.open(f'{image_folder}{filename}')
    clean_name = os.path.splitext(filename)[0]
    img.save(f'{output_folder}{clean_name}.png', 'png')
    img.close()