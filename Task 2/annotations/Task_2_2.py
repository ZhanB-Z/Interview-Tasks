from collections import defaultdict 
from Task_2_1 import load_tree

PATH = "/Users/zhan/Desktop/Python/Task 2/annotations"

all_roots = load_tree(PATH)

class_statistics = defaultdict(int)

unique_figures = []  
def get_unique_figures(root):
    for child in root.find(".//image").iter():
        if child.tag != 'image':
            figure_name = child.tag
            if figure_name not in unique_figures:
                unique_figures.append(figure_name)
    print(unique_figures)
    return unique_figures


# 4: Статистика по классам
def count_stats(root, list):
    class_statistics = {}
    for image in root.findall('image'):
        for label in image.findall('.//*'):
            if label.tag in list:
                class_label = label.get('label')

                class_statistics[class_label] = class_statistics.get(class_label, 0) + 1

    for class_label, count in class_statistics.items():
        print(f"Class {class_label}: {count} ")


if __name__ == "__main__":
    for file_name, root in all_roots.items():
        print(f"Counting CLASS stats for file {file_name}")
        get_unique_figures(root)
        count_stats(root, list=unique_figures)


        
