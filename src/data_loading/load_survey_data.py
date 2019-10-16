from typing import List

from src.data_loading.file_parser import parse_survey_file
from src.data_loading.row_splitter import split_response_rows
from src.data_loading.response_parser import parse_raw_responses
from src.data_loading.row_differentiator import RowDifferentiator
from src.survey_response import SurveyResponse
from src.utils import load_config

def load_survey_data() -> List[SurveyResponse]:
    row_differentiator = make_row_differentiator()
    raw_data = parse_survey_file(load_config()['response_data_filepath'])
    split_data = split_response_rows(raw_data, row_differentiator)
    return parse_raw_responses(split_data)

def make_row_differentiator() -> RowDifferentiator:
    PRIMARY_ACTIVITY_FIELD_NAME = 'Q1'
    row_differentiator = RowDifferentiator(PRIMARY_ACTIVITY_FIELD_NAME)
    row_differentiator.add_mapping('1', 'internship')
    row_differentiator.add_mapping('2', 'internship')
    row_differentiator.add_mapping('3', 'summer_job')
    row_differentiator.add_mapping('4', 'research')
    row_differentiator.add_mapping('5', 'research')
    row_differentiator.add_mapping('6', 'additional_study')
    row_differentiator.add_mapping('7', 'volunteering')
    row_differentiator.add_mapping('8', 'vacation')
    row_differentiator.add_mapping('9', 'other')
    return row_differentiator