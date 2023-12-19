import xml.etree.ElementTree as ET 
from collections import defaultdict
import os

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
        # print(f"Successfully parsed file {file}")
        roots[file] = root
    # print(roots)
    return roots    

all_roots = load_tree(PATH)

# 1 Всего изображений
def count_images(root):
    image_count = 0
    for image in root.findall('image'):
        image_count += 1
    print(f"The total number of images is: {image_count}")

# 2. Всего изображений размечено
def count_marked(root):
    marked_images = 0
    for image in root.findall('image'):
       if any(image.iter()):
            marked_images += 1
    print(f"The total number of marked images is: {marked_images}")

# 3. Сколько (если есть) неразмеченных изображений
def count_unmarked(root):
    unmarked_images = 0
    for image in root.findall('image'):
        if not any(image.iter()):
            unmarked_images += 1
    
    print(f"The total number of unmarked images is: {unmarked_images}")

# 5: Количество фигур (всего). Статистика по фигурам:
def total_figures(root):
    figure_statistics = defaultdict(int)
    for image in root.findall('image'):
        for figure in image:
            figure_type = figure.tag
            figure_statistics[figure_type] += 1

    total_figures = sum(figure_statistics.values())
    print(f"Total number of figures: {total_figures}")

# 6: Название и параметры (широта, высота) самого большого изображения и самого маленького
def largest_and_smallest(root):
    max_size = 0
    min_size = float('inf')

    max_images = []
    min_images =[]

    for image in root.findall('image'):
        width = int(image.get('width'))
        height = int(image.get('height'))

        size = width * height 
        name = image.get('name')

        if size > max_size:
            max_size = size
            max_images = [(name, width, height)]
        elif size == max_size:
            max_images.append((name, width, height))
        
        if size < min_size:
            min_size = size
            min_images = [(name, width, height)]
        elif size == min_size:
            min_images.append((name, width, height))

    if len(max_images) == 1:
        print(f"The largest image is {max_images[0]}")
    else:
        print(f"The number of largest images is {len(max_images)}")
        print(f"Here is one example: {max_images[0]}")

    if len(min_images) == 1:
        print(f"The smallest images is {min_images[0]}")
    else:
        print(f"The number of smallest images is {len(min_images)}")
        print(f"Here is one example: {min_images[0]}")



def General_Statistics(root):
    count_images(root)
    count_marked(root)
    count_unmarked(root)    
    total_figures(root)
    largest_and_smallest(root)
    

if __name__ == "__main__":
    for file_name, root in all_roots.items():
        print(f"Counting stats for file {file_name}")
        General_Statistics(root)
        print("Next file... \n")

