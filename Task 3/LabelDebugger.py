from PIL import Image, ImageDraw
import os
import xml.etree.ElementTree as ET 
from Masks_Updated import load_masks_from_xml

images_path = "/Users/zhan/Desktop/Python/Task 3/images"
save_path = "/Users/zhan/Desktop/Python/Task 3/modified_images"

xml_file_path = "/Users/zhan/Desktop/Python/Task 3/masks.xml"
masks_data = load_masks_from_xml(xml_file_path)

def debug_ignore(image_path, masks, save_path):
    debug_image = Image.open(image_path)

    debug_draw = ImageDraw.Draw(debug_image)
    for mask in masks:
        if mask['label'] == 'Ignore':
            debug_draw.polygon(mask['points'], outline=(255, 0, 0))
            # debug_draw.polygon(mask['points'], fill=0) 
        else: 
            debug_draw.polygon(mask['points'], outline=(0,255,0))

    file_name = os.path.splitext(os.path.basename(image_path))[0]
    debug_image.save(os.path.join(save_path, f'debug_{file_name}.png'))
    print(f"Success, {file_name} was created")

for image_file in os.listdir(images_path):
    image_path = os.path.join(images_path, image_file)
    if not image_file.lower().endswith(('.png','jpg')):
        print(f"Skipping non-image file: {image_file}")
        continue

    image = Image.open(image_path)
    file_name = os.path.splitext(os.path.basename(image_path))[0]

    if image_file in masks_data:
        debug_ignore(image_path, masks_data[image_file], save_path)
        