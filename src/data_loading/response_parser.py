from datetime import datetime
from typing import Union, List, Any
from src.survey_response import SurveyResponse


class RawResponseParser:

    def __init__(self, raw_data: dict):
        self._raw_data = raw_data

    def parse(self) -> SurveyResponse:
        return SurveyResponse(
            response_datetime=self._get_processed_value_or_none(self._raw_data['RecordedDate'], self._parse_datetime_str),
            qualtrics_response_id=self._get_processed_value_or_none(self._raw_data['ResponseId'], self._keep_value_unchanged),
            hopkins_id=self._get_processed_value_or_none(self._raw_data['ExternalReference'], self._keep_value_unchanged),
            activity_type=self._get_value_from_combined_fields('Q1', 'Q1_9_TEXT', self._keep_value_unchanged),
            location=self._get_processed_value_or_none(self._raw_data['Q3'], self._keep_value_unchanged),
            org_name=self._get_processed_value_or_none(self._raw_data['Q4'], self._keep_value_unchanged),
            org_subdivision=self._get_processed_value_or_none(self._raw_data['Q5'], self._keep_value_unchanged),
            activity_description=self._get_processed_value_or_none(self._raw_data['Q6'], self._keep_value_unchanged),
            research_subject=self._get_processed_value_or_none(self._raw_data['Q7'], self._keep_value_unchanged),
            length_in_weeks=self._get_processed_value_or_none(self._raw_data['Q8'], int),
            experience_was_paid=self._get_processed_value_or_none(self._raw_data['Q9'], self._response_is_yes),
            pay_rate_usd=self._get_processed_value_or_none(self._raw_data['Q10'], int),
            pay_frequency=self._get_value_from_combined_fields('Q10_2', 'Q10_5_TEXT', self._keep_value_unchanged),
            non_salary_benefits=self._get_list_from_combined_fields('Q11', 'Q11_4_TEXT'),
            received_grant_funding=self._get_processed_value_or_none(self._raw_data['Q19'], self._response_is_yes),
            grant_org_name=self._get_processed_value_or_none(self._raw_data['Q12'], self._keep_value_unchanged),
            grant_award_name=self._get_processed_value_or_none(self._raw_data['Q13'], self._keep_value_unchanged),
            student_is_receiving_credit=self._get_processed_value_or_none(self._raw_data['Q14'], self._response_is_yes),
            net_promoter_score=self._get_processed_value_or_none(self._raw_data['Q15'], int),
            additional_comments=self._get_processed_value_or_none(self._raw_data['Q18'], self._keep_value_unchanged),
            supportive_staff=self._get_processed_value_or_none(self._raw_data['Q16'], self._keep_value_unchanged),
            is_willing_to_share_experience=self._get_processed_value_or_none(self._raw_data['Q17'], self._response_is_yes)
        )

    def _get_value_from_combined_fields(self, main_field: str, other_field: str, processor_func: callable) -> Union[str, None]:
        if self._raw_data[other_field] != '':
            return self._raw_data[other_field]
        else:
            return self._get_processed_value_or_none(self._raw_data[main_field], processor_func)

    def _get_list_from_combined_fields(self, main_field: str, other_field: str) -> Union[List[str], None]:
        main_list = self._get_processed_value_or_none(self._raw_data[main_field], self._parse_list_str)
        if main_list and 'Other:' in main_list:
            main_list[main_list.index('Other:')] = self._raw_data[other_field]
        return main_list


    def _get_processed_value_or_none(self, value: str, processor_func: callable) -> Union[Any, None]:
        if value == '':
            return None
        else:
            return processor_func(value)

    @staticmethod
    def _parse_datetime_str(datetime_str: str) -> datetime:
        return datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')

    @staticmethod
    def _parse_list_str(list_str: str) -> List[str]:
        return list_str.split(',')

    @staticmethod
    def _response_is_yes(response: str) -> bool:
        return response == 'Yes'

    @staticmethod
    def _keep_value_unchanged(value: str) -> str:
        return value
