from datetime import datetime
from typing import Union, List

class SurveyResponse:

    def __init__(self, response_datetime: datetime = None, qualtrics_response_id: str = None,
                 hopkins_id: str = None, activity_type: str = None, location: str = None,
                 org_name: str = None, org_subdivision: str = None, activity_description: str = None,
                 research_subject: str = None, length_in_weeks: int = None, experience_was_paid: bool = None,
                 pay_rate_usd: int = None, pay_frequency: str = None, non_salary_benefits = None,
                 received_grant_funding: bool = None, grant_org_name: str = None,
                 grant_award_name: str = None, student_is_receiving_credit: bool = None,
                 net_promoter_score: int = None, additional_comments: str = None,
                 supportive_staff: str = None, is_willing_to_share_experience: bool = None):

        self._data = {
            'response_datetime': response_datetime,
            'qualtrics_response_id': qualtrics_response_id,
            'hopkins_id': hopkins_id,
            'activity_type': activity_type,
            'location': location,
            'org_name': org_name,
            'org_subdivision': org_subdivision,
            'activity_description': activity_description,
            'research_subject': research_subject,
            'length_in_weeks': length_in_weeks,
            'experience_was_paid': experience_was_paid,
            'pay_rate_usd': pay_rate_usd,
            'pay_frequency': pay_frequency,
            'non_salary_benefits': non_salary_benefits,
            'received_grant_funding': received_grant_funding,
            'grant_org_name': grant_org_name,
            'grant_award_name': grant_award_name,
            'student_is_receiving_credit': student_is_receiving_credit,
            'net_promoter_score': net_promoter_score,
            'additional_comments': additional_comments,
            'supportive_faculty': supportive_staff,
            'is_willing_to_share_experience': is_willing_to_share_experience,
        }

    def to_dict(self) -> dict:
        return self._data.copy()

    def __eq__(self, other: 'SurveyResponse') -> bool:
        return self.to_dict() == other.to_dict()


def create_survey_response(raw_response_data: dict) -> SurveyResponse:

    def _get_value_from_combined_fields(raw_data: dict, main_field: str, other_field: str) -> Union[str, None]:
        if raw_data[other_field] != '':
            return raw_data[other_field]
        else:
            return _get_nonempty_str_or_none(raw_data[main_field])

    def _get_nonempty_str_or_none(value: str) -> Union[str, None]:
        if value == '':
            return None
        else:
            return value

    def _get_datetime_or_none(value: str) -> Union[datetime, None]:
        if value == '':
            return None
        else:
            return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')

    def _get_int_or_none(value: str) -> Union[int, None]:
        if value == '':
            return None
        else:
            return int(value)

    def _get_bool_or_none(value: str, bool_func: callable) -> Union[bool, None]:
        if value == '':
            return None
        else:
            return bool_func(value)

    def _response_is_yes(response: str) -> bool:
        return response == 'Yes'

    return SurveyResponse(
        response_datetime=_get_datetime_or_none(raw_response_data['RecordedDate']),
        qualtrics_response_id=_get_nonempty_str_or_none(raw_response_data['ResponseId']),
        hopkins_id=_get_nonempty_str_or_none(raw_response_data['ExternalReference']),
        activity_type=_get_value_from_combined_fields(raw_response_data, 'Q1', 'Q1_9_TEXT'),
        location=_get_nonempty_str_or_none(raw_response_data['Q3']),
        org_name=_get_nonempty_str_or_none(raw_response_data['Q4']),
        org_subdivision=_get_nonempty_str_or_none(raw_response_data['Q5']),
        activity_description=_get_nonempty_str_or_none(raw_response_data['Q6']),
        research_subject=_get_nonempty_str_or_none(raw_response_data['Q7']),
        length_in_weeks=_get_int_or_none(raw_response_data['Q8']),
        experience_was_paid=_get_bool_or_none(raw_response_data['Q9'], _response_is_yes),
        pay_rate_usd=_get_int_or_none(raw_response_data['Q10']),
        pay_frequency=_get_value_from_combined_fields(raw_response_data, 'Q10_2', 'Q10_5_TEXT'),
        non_salary_benefits=_get_value_from_combined_fields(raw_response_data, 'Q11', 'Q11_4_TEXT'),
        received_grant_funding=_get_bool_or_none(raw_response_data['Q19'], _response_is_yes),
        grant_org_name=_get_nonempty_str_or_none(raw_response_data['Q12']),
        grant_award_name=_get_nonempty_str_or_none(raw_response_data['Q13']),
        student_is_receiving_credit=_get_bool_or_none(raw_response_data['Q14'], _response_is_yes),
        net_promoter_score=_get_int_or_none(raw_response_data['Q15']),
        additional_comments=_get_nonempty_str_or_none(raw_response_data['Q18']),
        supportive_staff=_get_nonempty_str_or_none(raw_response_data['Q16']),
        is_willing_to_share_experience=_get_bool_or_none(raw_response_data['Q17'], _response_is_yes)
    )