from typing import List

from src.extract.file_parser import parse_survey_file
from src.extract.row_splitter import split_response_rows
from src.extract.response_parser import parse_raw_responses
from src.extract.row_differentiator import RowDifferentiator
from src.survey_response import SurveyResponse

def extract_survey_data(raw_data_filepath: str) -> List[SurveyResponse]:
    row_differentiator = make_row_differentiator()
    raw_data = parse_survey_file(raw_data_filepath)
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