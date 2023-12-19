import xml.etree.ElementTree as ET 
import os
from Task_2_1 import load_tree

script_directory = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(script_directory, "annotations")

def load_tree(directory_path):
    roots = {}
    for file in os.listdir(directory_path):
        if not file.lower().endswith('.xml'):
            print(f"Skipping the irrelevant file: {file}")
            continue
        file_path = os.path.join(directory_path, file)
        tree = ET.parse(file_path)
        root = tree.getroot()
        roots[file] = (root, tree)  
    return roots

all_roots = load_tree(PATH)


#Task 7: Изменить id-шники изображений - сделать их в обратном порядке.
def invert_ids(root, tree, file_name):
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
    # tree.write(f"{file_name}_modified.xml")
    print("Success")

#Task 8 Изменить name изображений - поменять расширение на 'png'.
def convert_to_png(root, tree, file_name):
    for image in root.findall('image'):
        name = image.get('name')
        base, _ = name.rsplit(".", 1)
        new_name = f"{base}.png"
        image.set("name", new_name)

    # tree.write(f"{file_name}_modified.xml")
    print("Success")

#Task 9 Изменить name изображений - удалить путь к файлу, оставить только название самого файла.
def change_name(root, tree, file_name):
    for image in root.findall('image'):
        full_path = image.get('name')
        full_name = os.path.basename(full_path)
        image.set('name', full_name)

    # tree.write(f"{file_name}_modified.xml")
    print("Success")

def modify_file(root, tree, file_name):
    invert_ids(root, tree, file_name)
    convert_to_png(root, tree, file_name)
    change_name(root,tree,file_name)
    tree.write(f"{file_name}_modified.xml")



if __name__ == "__main__":
    for file_name, (root, tree) in all_roots.items():
        print(f"Starting to perform amendmendts...")
        modify_file(root,tree,file_name)
        
