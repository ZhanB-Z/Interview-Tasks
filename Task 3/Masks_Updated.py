from PIL import Image, ImageDraw
import os
import xml.etree.ElementTree as ET 

def load_masks_from_xml(xml_file_path):
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    masks_data = {}

    for image in root.findall('image'):
        image_name = image.get('name').split('/')[-1]
        masks = []

        for polygon in image.findall('polygon'):
            label = polygon.get("label")
            points = polygon.get("points").split(";")
            points = [tuple(map(float, point.split(","))) for point in points]
            masks.append({"label": label, "points": points})

            masks_data[image_name] = masks

    # print(masks_data)
    return masks_data

xml_file_path = "/Users/zhan/Desktop/Python/Task 3/masks.xml"
masks_data = load_masks_from_xml(xml_file_path)

images_path = "/Users/zhan/Desktop/Python/Task 3/images"
save_path = "/Users/zhan/Desktop/Python/Task 3/modified_images"


def create_black_background_mask(image_size, masks, save_path, file_name):

    black_mask = Image.new("RGB", image_size, (0, 0, 0))
    draw_black = ImageDraw.Draw(black_mask)


    for mask in masks:
        # print(mask['label'])
        if mask['label'].lower() != 'ignore':
            # print(mask['points'])
            draw_black.polygon(mask['points'], fill=(128, 0, 128))

    for mask in masks:
        if mask['label'].lower() == 'ignore':
            draw_black.polygon(mask['points'], fill=(0, 0, 0)) 

    black_mask.save(os.path.join(save_path, f'black_background_{file_name}.png'))
    print("Black background mask created and saved successfully.")


def create_transparent_mask(image_path, masks, save_path):
    original_image = Image.open(image_path).convert("RGBA")

    mask_alpha = Image.new('L', original_image.size, 255)
    draw_alpha = ImageDraw.Draw(mask_alpha)

    for mask in masks:
        if mask['label'].lower() == 'ignore':
            # print(mask['points'])
            draw_alpha.polygon(mask['points'], fill=0)    
    
    draw_original = ImageDraw.Draw(original_image)

    for mask in masks:
        if mask['label'].lower() != 'ignore':
            draw_original.polygon(mask['points'], fill=(128,0,128))    
    
    original_image.putalpha(mask_alpha)

    file_name = os.path.splitext(os.path.basename(image_path))[0]
    original_image.save(os.path.join(save_path, f'masked_{file_name}.png'))
    print("Original image mask created and saved successfully.")


for image_file in os.listdir(images_path):
    image_path = os.path.join(images_path, image_file)
    if not image_file.lower().endswith(('.png', 'jpg')):
        print(f"Skipping non-image file: {image_file}")
        continue

    image = Image.open(image_path)
    file_name = os.path.splitext(os.path.basename(image_path))[0]

    if image_file in masks_data:
        create_transparent_mask(image_path, masks_data[image_file], save_path)
        create_black_background_mask(image.size, masks_data[image_file], save_path, file_name)
