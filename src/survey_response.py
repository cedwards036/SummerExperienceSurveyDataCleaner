from datetime import datetime

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