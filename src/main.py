import json

from src.data_loading.file_parser import parse_survey_file
from src.data_loading.row_splitter import split_response_rows
from definitions import CONFIG_PATH

def load_config() -> dict:
    with open(CONFIG_PATH, encoding='utf-8') as file:
        return json.load(file)

if __name__ == '__main__':
    raw_data = parse_survey_file(load_config()['response_data_filepath'])
    split_data = split_response_rows(raw_data)
    for row in split_data:
        print(row)