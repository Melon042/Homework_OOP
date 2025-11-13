from src.classes import Category
import json


def get_category_objects_from_json_file(path_to_json_file):
    """Принимает путь до JSON-файла и возвращает список объектов класса Category"""

    with open(path_to_json_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    return [Category(category["name"], category["description"], category["products"]) for category in data]
