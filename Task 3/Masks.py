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

def create_masks(image_path, masks, save_path):
    print("Initiating mask creation function ....")
    image = Image.open(image_path)
    original_with_mask = image.copy()
    black_mask = Image.new("RGB", image.size, (0,0,0))
    
    mask_alpha = Image.new('L', image.size, 255)
    draw_alpha = ImageDraw.Draw(mask_alpha)
    draw_black = ImageDraw.Draw(black_mask)

    print("Starting creation of masks ....")
    for mask in masks:
        if mask['label'].lower() == 'ignore':
            draw_alpha.polygon(mask['points'], fill=0)
            draw_black.polygon(mask['points'], fill='black')

    original_with_mask.putalpha(mask_alpha)
    
    print("Applying other masks ...")
    for mask in masks:
        if mask['label'].lower() != 'ignore':
            ImageDraw.Draw(original_with_mask).polygon(mask['points'], fill=(128, 0, 128))
            ImageDraw.Draw(black_mask).polygon(mask['points'], fill=(128, 0, 128))

    original_with_mask.save(os.path.join(save_path, f'masked_{os.path.splitext(os.path.basename(image_path))[0]}.png'))
    black_mask.save(os.path.join(save_path, f'black_mask_{os.path.splitext(os.path.basename(image_path))[0]}.png'))
    print("Masks created and saved successfully.")

images_path = "/Users/zhan/Desktop/Python/Task 3/images"
save_path = "/Users/zhan/Desktop/Python/Task 3/modified_images"

for image_file in os.listdir(images_path):
    image_path = os.path.join(images_path, image_file)
    if image_file in masks_data:
        create_masks(image_path, masks_data[image_file], save_path)