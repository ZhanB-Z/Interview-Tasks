import xml.etree.ElementTree as ET 
from collections import defaultdict

tree = ET.parse("/Users/zhan/Desktop/Python/Task 2/annotations3.xml")
root = tree.getroot()

# проверка парскинга
def ParseXML(root):
    for child in root:
        print(child.tag, child.attrib)
        for subchild in child:
            print(subchild.tag, subchild.attrib)


# 1 Всего изображений
def CountImages(root):
    image_count = 0
    for image in root.findall('image'):
        image_count += 1
    print(f"The total number of images is: {image_count}")

CountImages(root)

# 2. Всего изображений размечено
def CountMarked(root):
    marked_images = 0
    for image in root.findall('image'):
        if image.find('box') is not None:
            marked_images += 1
    print(f"The total number of marked images is: {marked_images}")

CountMarked(root)

# 3. (если есть) Неразмеченных изображений
def CountUnmarked(root):
    unmarked_images = 0
    for image in root.findall('image'):
        if image.find('box') is None:
            unmarked_images += 1
    
    print(f"The total number of unmarked images is: {unmarked_images}")

CountUnmarked(root)


#Task 5: Количество фигур (всего). Статистика по фигурам:
def FigureStats(root):
    figure_statistics = defaultdict(int)
    for image in root.findall('image'):
        for figure in image:
            figure_type = figure.tag
            figure_statistics[figure_type] += 1

    for figure_type, count in figure_statistics.items():
        print(f"{figure_type}: {count}")

    total_figures = sum(figure_statistics.values())
    print(f"Total number of figures: {total_figures}")

# FigureStats(root)

#Task 6: Название и параметры (широта, высота) самого большого изображения и самого маленького
def LargestAndSmallestImages(root):
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



