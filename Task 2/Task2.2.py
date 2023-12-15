import xml.etree.ElementTree as ET 
from collections import defaultdict 

tree = ET.parse("/Users/zhan/Desktop/Python/Task 2/annotations3.xml")
root = tree.getroot()

# Проверка парсинга
def ParseXML(root):
    for child in root:
        print(child.tag, child.attrib)
        for subchild in child:
            print(subchild.tag, subchild.attrib)

class_statistics = defaultdict(int)

#Task 4: Статистика по классам
def CountStats(root):
    for image in root.findall('image'):
        for box in image.findall('box'):
            class_label = box.get('label')
            class_statistics[class_label] += 1

    for class_label, count in class_statistics.items():
        print(f"Class {class_label}: {count} ")

CountStats(root)
