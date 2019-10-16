import json
from typing import List
import csv
from definitions import CONFIG_PATH

def load_config() -> dict:
    with open(CONFIG_PATH, encoding='utf-8') as file:
        return json.load(file)


def list_of_dicts_to_csv(filepath: str, data: List[dict]):
    header = data[0].keys()
    with open(filepath, 'w', encoding='utf-8') as file:
        dict_writer = csv.DictWriter(file, header, lineterminator='\n')
        dict_writer.writeheader()
        dict_writer.writerows(data)
    return filepath