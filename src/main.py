from src.data_loading.load_survey_data import load_survey_data
from src.utils import list_of_dicts_to_csv, load_config

if __name__ == '__main__':
    survey_data = load_survey_data()
    survey_data_dicts = [response.to_dict() for response in survey_data]
    list_of_dicts_to_csv(load_config()['output_filepath'], survey_data_dicts)
    for response in survey_data:
        print(response.to_dict())