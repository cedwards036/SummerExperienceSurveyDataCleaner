import unittest
from datetime import datetime

from src.extract.response_parser import RawResponseParser, parse_raw_responses
from src.survey_response import SurveyResponse


def assert_survey_responses_are_equal(test_obj, expected: SurveyResponse, actual: SurveyResponse):
    test_obj.assertEqual(expected.to_dict(), actual.to_dict())


class TestParseRawResponses(unittest.TestCase):

    def test_parse_responses(self):
        test_data = [
            {'StartDate': '2019-10-10 10:53:27', 'EndDate': '2019-10-13 23:39:48', 'Status': 'IP Address', 'IPAddress': '', 'Progress': '100', 'Duration (in seconds)': '305180',
             'Finished': 'True', 'RecordedDate': '2019-10-13 23:39:48', 'ResponseId': 'R_1jOM7xwHaTf91F1', 'RecipientLastName': '', 'RecipientFirstName': '', 'RecipientEmail': '',
             'ExternalReference': 'BH47TY', 'LocationLatitude': '', 'LocationLongitude': '', 'DistributionChannel': 'email', 'UserLanguage': 'EN',
             'Q1': 'Summer Job (working purely to earn money, e.g. as a waiter)', 'Q1_9_TEXT': '', 'Q16': 'Professor Talreja was great!', 'Q17': 'Yes', 'Q3': 'New Hampshire',
             'Q4': 'Camp Onaway', 'Q5': 'Scheduling', 'Q6': 'I was a camp scheduler', 'Q7': '', 'Q8': '9', 'Q9': 'Yes', 'Q10': '3400', 'Q10_2': 'Bi-weekly', 'Q10_5_TEXT': '',
             'Q11': 'Free or subsidized housing', 'Q11_4_TEXT': '', 'Q19': 'Yes', 'Q12': 'The Camp Scholarship Foundation', 'Q13': 'The Camp Scholarship', 'Q14': 'No',
             'Q15_NPS_GROUP': 'Passive', 'Q15': '8', 'Q18': 'I liked it, I guess'},
            {'StartDate': '', 'EndDate': '', 'Status': 'IP Address', 'IPAddress': '', 'Progress': '100', 'Duration (in seconds)': '305180',
             'Finished': 'True', 'RecordedDate': '2019-10-15 11:30:00', 'ResponseId': 'R_7gu$8fjGrug', 'RecipientLastName': '', 'RecipientFirstName': '', 'RecipientEmail': '',
             'ExternalReference': 'RTOAP5', 'LocationLatitude': '', 'LocationLongitude': '', 'DistributionChannel': 'email', 'UserLanguage': 'EN',
             'Q1': 'Internship', 'Q1_9_TEXT': '', 'Q16': '', 'Q17': 'No', 'Q3': 'Sacramento, California',
             'Q4': 'City Hall', 'Q5': '', 'Q6': 'I did admin stuff', 'Q7': '', 'Q8': '10', 'Q9': 'No', 'Q10': '', 'Q10_2': '', 'Q10_5_TEXT': '',
             'Q11': 'Transportation,Other:', 'Q11_4_TEXT': 'Food', 'Q19': 'No', 'Q12': '', 'Q13': '', 'Q14': 'Yes',
             'Q15_NPS_GROUP': 'Passive', 'Q15': '5', 'Q18': 'It wasn\'t special'}
        ]

        expected = [
            SurveyResponse(
                response_datetime=datetime(2019, 10, 13, 23, 39, 48),
                qualtrics_response_id='R_1jOM7xwHaTf91F1',
                hopkins_id='BH47TY',
                activity_type='Summer Job (working purely to earn money, e.g. as a waiter)',
                location='New Hampshire',
                org_name='Camp Onaway',
                org_subdivision='Scheduling',
                activity_description='I was a camp scheduler',
                research_subject=None,
                length_in_weeks=9,
                experience_was_paid=True,
                pay_rate_usd=3400.0,
                pay_frequency='Bi-weekly',
                non_salary_benefits=['Free or subsidized housing'],
                received_grant_funding=True,
                grant_org_name='The Camp Scholarship Foundation',
                grant_award_name='The Camp Scholarship',
                student_is_receiving_credit=False,
                net_promoter_score=8,
                additional_comments='I liked it, I guess',
                supportive_staff='Professor Talreja was great!',
                is_willing_to_share_experience=True
            ),
            SurveyResponse(
                response_datetime=datetime(2019, 10, 15, 11, 30, 00),
                qualtrics_response_id='R_7gu$8fjGrug',
                hopkins_id='RTOAP5',
                activity_type='Internship',
                location='Sacramento, California',
                org_name='City Hall',
                activity_description='I did admin stuff',
                length_in_weeks=10,
                experience_was_paid=False,
                non_salary_benefits=['Transportation', 'Food'],
                received_grant_funding=False,
                student_is_receiving_credit=True,
                net_promoter_score=5,
                additional_comments='It wasn\'t special',
                is_willing_to_share_experience=False
            )
        ]
        self.assertEqual(expected, parse_raw_responses(test_data))



class TestResponseParser(unittest.TestCase):

    def test_create_survey_response_from_raw_data(self):
        test_data = {'StartDate': '2019-10-10 10:53:27', 'EndDate': '2019-10-13 23:39:48', 'Status': 'IP Address', 'IPAddress': '', 'Progress': '100', 'Duration (in seconds)': '305180',
                     'Finished': 'True', 'RecordedDate': '2019-10-13 23:39:48', 'ResponseId': 'R_1jOM7xwHaTf91F1', 'RecipientLastName': '', 'RecipientFirstName': '', 'RecipientEmail': '',
                     'ExternalReference': 'BH47TY', 'LocationLatitude': '', 'LocationLongitude': '', 'DistributionChannel': 'email', 'UserLanguage': 'EN',
                     'Q1': 'Summer Job (working purely to earn money, e.g. as a waiter)', 'Q1_9_TEXT': '', 'Q16': 'Professor Talreja was great!', 'Q17': 'Yes', 'Q3': 'New Hampshire',
                     'Q4': 'Camp Onaway', 'Q5': 'Scheduling', 'Q6': 'I was a camp scheduler', 'Q7': '', 'Q8': '9', 'Q9': 'Yes', 'Q10': '3400.50', 'Q10_2': 'Bi-weekly', 'Q10_5_TEXT': '',
                     'Q11': 'Free or subsidized housing', 'Q11_4_TEXT': '', 'Q19': 'Yes', 'Q12': 'The Camp Scholarship Foundation', 'Q13': 'The Camp Scholarship', 'Q14': 'No',
                     'Q15_NPS_GROUP': 'Passive', 'Q15': '8', 'Q18': 'I liked it, I guess'}
        expected = SurveyResponse(
            response_datetime=datetime(2019, 10, 13, 23, 39, 48),
            qualtrics_response_id='R_1jOM7xwHaTf91F1',
            hopkins_id='BH47TY',
            activity_type='Summer Job (working purely to earn money, e.g. as a waiter)',
            location='New Hampshire',
            org_name='Camp Onaway',
            org_subdivision='Scheduling',
            activity_description='I was a camp scheduler',
            research_subject=None,
            length_in_weeks=9,
            experience_was_paid=True,
            pay_rate_usd=3400.5,
            pay_frequency='Bi-weekly',
            non_salary_benefits=['Free or subsidized housing'],
            received_grant_funding=True,
            grant_org_name='The Camp Scholarship Foundation',
            grant_award_name='The Camp Scholarship',
            student_is_receiving_credit=False,
            net_promoter_score=8,
            additional_comments='I liked it, I guess',
            supportive_staff='Professor Talreja was great!',
            is_willing_to_share_experience=True
        )
        assert_survey_responses_are_equal(self, expected, RawResponseParser(test_data).parse())

    def test_create_survey_response_translates_empty_str_to_none(self):
        test_data = {'StartDate': '', 'EndDate': '', 'Status': '', 'IPAddress': '', 'Progress': '', 'Duration (in seconds)': '',
                     'Finished': '', 'RecordedDate': '', 'ResponseId': '', 'RecipientLastName': '', 'RecipientFirstName': '', 'RecipientEmail': '',
                     'ExternalReference': '', 'LocationLatitude': '', 'LocationLongitude': '', 'DistributionChannel': '', 'UserLanguage': '',
                     'Q1': '', 'Q1_9_TEXT': '', 'Q16': '', 'Q17': '', 'Q3': '',
                     'Q4': '', 'Q5': '', 'Q6': '', 'Q7': '', 'Q8': '', 'Q9': '', 'Q10': '', 'Q10_2': '', 'Q10_5_TEXT': '',
                     'Q11': '', 'Q11_4_TEXT': '', 'Q19': '', 'Q12': '', 'Q13': '', 'Q14': '',
                     'Q15_NPS_GROUP': '', 'Q15': '', 'Q18': ''}
        assert_survey_responses_are_equal(self, SurveyResponse(), RawResponseParser(test_data).parse())

    def test_fields_with_other_freetext_are_merged_properly(self):
        test_data_with_others = {'StartDate': '', 'EndDate': '', 'Status': '', 'IPAddress': '', 'Progress': '', 'Duration (in seconds)': '',
                                 'Finished': '', 'RecordedDate': '', 'ResponseId': '', 'RecipientLastName': '', 'RecipientFirstName': '', 'RecipientEmail': '',
                                 'ExternalReference': '', 'LocationLatitude': '', 'LocationLongitude': '', 'DistributionChannel': '', 'UserLanguage': '',
                                 'Q1': 'Other', 'Q1_9_TEXT': 'Travelled to Mars', 'Q16': '', 'Q17': '', 'Q3': '',
                                 'Q4': '', 'Q5': '', 'Q6': '', 'Q7': '', 'Q8': '', 'Q9': '', 'Q10': '', 'Q10_2': 'Other', 'Q10_5_TEXT': 'I was paid before I started',
                                 'Q11': 'Other:', 'Q11_4_TEXT': 'Free Food', 'Q19': '', 'Q12': '', 'Q13': '', 'Q14': '',
                                 'Q15_NPS_GROUP': '', 'Q15': '', 'Q18': ''}
        expected = SurveyResponse(
            activity_type='Travelled to Mars',
            pay_frequency='I was paid before I started',
            non_salary_benefits=['Free Food']
        )
        assert_survey_responses_are_equal(self, expected, RawResponseParser(test_data_with_others).parse())

    def test_multiple_non_salary_benefits_are_broken_into_list(self):
        test_data_with_other = {'StartDate': '', 'EndDate': '', 'Status': '', 'IPAddress': '', 'Progress': '', 'Duration (in seconds)': '',
                                'Finished': '', 'RecordedDate': '', 'ResponseId': '', 'RecipientLastName': '', 'RecipientFirstName': '', 'RecipientEmail': '',
                                'ExternalReference': '', 'LocationLatitude': '', 'LocationLongitude': '', 'DistributionChannel': '', 'UserLanguage': '',
                                'Q1': '', 'Q1_9_TEXT': '', 'Q16': '', 'Q17': '', 'Q3': '',
                                'Q4': '', 'Q5': '', 'Q6': '', 'Q7': '', 'Q8': '', 'Q9': '', 'Q10': '', 'Q10_2': '', 'Q10_5_TEXT': '',
                                'Q11': 'Housing,Transportation,Other:', 'Q11_4_TEXT': 'Free Food', 'Q19': '', 'Q12': '', 'Q13': '', 'Q14': '',
                                'Q15_NPS_GROUP': '', 'Q15': '', 'Q18': ''}
        expected_from_other = SurveyResponse(
            non_salary_benefits=['Housing', 'Transportation', 'Free Food']
        )
        assert_survey_responses_are_equal(self, expected_from_other, RawResponseParser(test_data_with_other).parse())

        test_plain_data = {'StartDate': '', 'EndDate': '', 'Status': '', 'IPAddress': '', 'Progress': '', 'Duration (in seconds)': '',
                           'Finished': '', 'RecordedDate': '', 'ResponseId': '', 'RecipientLastName': '', 'RecipientFirstName': '', 'RecipientEmail': '',
                           'ExternalReference': '', 'LocationLatitude': '', 'LocationLongitude': '', 'DistributionChannel': '', 'UserLanguage': '',
                           'Q1': '', 'Q1_9_TEXT': '', 'Q16': '', 'Q17': '', 'Q3': '',
                           'Q4': '', 'Q5': '', 'Q6': '', 'Q7': '', 'Q8': '', 'Q9': '', 'Q10': '', 'Q10_2': '', 'Q10_5_TEXT': '',
                           'Q11': 'Housing,Transportation', 'Q11_4_TEXT': '', 'Q19': '', 'Q12': '', 'Q13': '', 'Q14': '',
                           'Q15_NPS_GROUP': '', 'Q15': '', 'Q18': ''}
        expected_from_plain = SurveyResponse(
            non_salary_benefits=['Housing', 'Transportation']
        )
        assert_survey_responses_are_equal(self, expected_from_plain, RawResponseParser(test_plain_data).parse())
