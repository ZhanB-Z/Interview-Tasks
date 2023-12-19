from collections import defaultdict 
from Task_2_1 import load_tree

PATH = "/Users/zhan/Desktop/Python/Task 2/annotations"

all_roots = load_tree(PATH)


#Task 5*: Количество фигур (box, polygon, etc). Статистика по фигурам:
def total_figures(root):
    figure_statistics = defaultdict(int)
    for image in root.findall('image'):
        for figure in image:
            figure_type = figure.tag
            figure_statistics[figure_type] += 1

    for figure_type, count in figure_statistics.items():
        print(f"{figure_type}: {count}")

    total_figures = sum(figure_statistics.values())
    print(f"Total number of figures: {total_figures}")


if __name__ == "__main__":
    for file_name, root in all_roots.items():
        print(f"Counting FIGURE stats for file {file_name}")
        total_figures(root)
        