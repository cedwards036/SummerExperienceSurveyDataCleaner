import unittest
from src.file_parser import parse_header, parse_survey_file

FILEPATH = 'test_input_file.csv'

class TestFileParser(unittest.TestCase):

    def test_parse_header(self):
        expected = ['StartDate', 'EndDate', 'Status', 'IPAddress', 'Progress', 'Duration (in seconds)', 'Finished', 'RecordedDate', 'ResponseId', 'RecipientLastName', 'RecipientFirstName', 'RecipientEmail', 'ExternalReference', 'LocationLatitude', 'LocationLongitude', 'DistributionChannel', 'UserLanguage', 'Q1', 'Q1_9_TEXT', '1_Q3', '1_Q4', '1_Q5', '1_Q6', '1_Q7', '1_Q8', '1_Q9', '1_Q10', '1_Q10_2', '1_Q10_5_TEXT', '1_Q11', '1_Q11_4_TEXT', '1_Q19', '1_Q12', '1_Q13', '1_Q14', '1_Q15_NPS_GROUP', '1_Q15', '1_Q18', '2_Q3', '2_Q4', '2_Q5', '2_Q6', '2_Q7', '2_Q8', '2_Q9', '2_Q10', '2_Q10_2', '2_Q10_5_TEXT', '2_Q11', '2_Q11_4_TEXT', '2_Q19', '2_Q12', '2_Q13', '2_Q14', '2_Q15_NPS_GROUP', '2_Q15', '2_Q18', '3_Q3', '3_Q4', '3_Q5', '3_Q6', '3_Q7', '3_Q8', '3_Q9', '3_Q10', '3_Q10_2', '3_Q10_5_TEXT', '3_Q11', '3_Q11_4_TEXT', '3_Q19', '3_Q12', '3_Q13', '3_Q14', '3_Q15_NPS_GROUP', '3_Q15', '3_Q18', '4_Q3', '4_Q4', '4_Q5', '4_Q6', '4_Q7', '4_Q8', '4_Q9', '4_Q10', '4_Q10_2', '4_Q10_5_TEXT', '4_Q11', '4_Q11_4_TEXT', '4_Q19', '4_Q12', '4_Q13', '4_Q14', '4_Q15_NPS_GROUP', '4_Q15', '4_Q18', '5_Q3', '5_Q4', '5_Q5', '5_Q6', '5_Q7', '5_Q8', '5_Q9', '5_Q10', '5_Q10_2', '5_Q10_5_TEXT', '5_Q11', '5_Q11_4_TEXT', '5_Q19', '5_Q12', '5_Q13', '5_Q14', '5_Q15_NPS_GROUP', '5_Q15', '5_Q18', '6_Q3', '6_Q4', '6_Q5', '6_Q6', '6_Q7', '6_Q8', '6_Q9', '6_Q10', '6_Q10_2', '6_Q10_5_TEXT', '6_Q11', '6_Q11_4_TEXT', '6_Q19', '6_Q12', '6_Q13', '6_Q14', '6_Q15_NPS_GROUP', '6_Q15', '6_Q18', '7_Q3', '7_Q4', '7_Q5', '7_Q6', '7_Q7', '7_Q8', '7_Q9', '7_Q10', '7_Q10_2', '7_Q10_5_TEXT', '7_Q11', '7_Q11_4_TEXT', '7_Q19', '7_Q12', '7_Q13', '7_Q14', '7_Q15_NPS_GROUP', '7_Q15', '7_Q18', '8_Q3', '8_Q4', '8_Q5', '8_Q6', '8_Q7', '8_Q8', '8_Q9', '8_Q10', '8_Q10_2', '8_Q10_5_TEXT', '8_Q11', '8_Q11_4_TEXT', '8_Q19', '8_Q12', '8_Q13', '8_Q14', '8_Q15_NPS_GROUP', '8_Q15', '8_Q18', '9_Q3', '9_Q4', '9_Q5', '9_Q6', '9_Q7', '9_Q8', '9_Q9', '9_Q10', '9_Q10_2', '9_Q10_5_TEXT', '9_Q11', '9_Q11_4_TEXT', '9_Q19', '9_Q12', '9_Q13', '9_Q14', '9_Q15_NPS_GROUP', '9_Q15', '9_Q18', 'Q16', 'Q17']
        with open(FILEPATH) as file:
            self.assertEqual(expected, parse_header(file))

    def test_parse_file(self):
        actual = parse_survey_file(FILEPATH)
        self.assertEqual(3, len(actual))
        with open(FILEPATH) as file:
            header = parse_header(file)
            for row in actual:
                self.assertEqual(header, list(row.keys()))
        self.assertEqual('TU73R3', actual[0]['ExternalReference'])
        self.assertEqual('', actual[2]['Q1_9_TEXT'])
        self.assertEqual('No', actual[1]['Q17'])