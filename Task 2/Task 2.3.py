import xml.etree.ElementTree as ET 
import os


tree = ET.parse("/Users/zhan/Desktop/Python/Task 2/annotations1.xml")
root = tree.getroot()

def ParseXML(root):
    for child in root:
        print(child.tag, child.attrib)
        for subchild in child:
            print(subchild.tag, subchild.attrib)

#Task 7: Изменить id-шники изображений - сделать их в обратном порядке.
def invertIDs(root):
    ids = []
    for image in root.findall('image'):
        image_id = image.get('id')
        ids.append(image_id)
    
    reversed_ids = list(reversed(ids))

    for image, new_id in zip(root.findall('image'), reversed_ids):
        image.set('id', new_id)
    
    check_id = []
    for image in root.findall('image'):
        image_id = image.get('id')
        check_id.append(image_id)
    
    # print(check_id)

    tree.write('modified_file.xml')
    print("Success")

#Task 8 Изменить name изображений - поменять расширение на 'png'.
def convertToPNG(root):
    for image in root.findall('image'):
        name = image.get('name')
        base, _ = name.rsplit(".", 1)
        new_name = f"{base}.png"
        image.set("name", new_name)

    tree.write('pngformat.xml')
    print("Success")

#Task 9 Изменить name изображений - удалить путь к файлу, оставить только название самого файла.
def modifyName(root):
    for image in root.findall('image'):
        full_path = image.get('name')
        full_name = os.path.basename(full_path)

        image.set('name', full_name)

    tree.write('cleanname.xml')
    print("Success")

modifyName(root)