import unittest

from src.extract.row_differentiator import RowDifferentiator
from src.extract.row_splitter import _split_row_into_multiple_responses, split_response_rows


class TestRowSplitter(unittest.TestCase):

    def setUp(self) -> None:
        self.row_differentiator = RowDifferentiator('Q1')
        self.row_differentiator.add_mapping('1', 'Internship')
        self.row_differentiator.add_mapping('2', 'Research')
        self.row_differentiator.add_mapping('3', 'Fellowship')
        self.row_differentiator.add_mapping('4', 'Vacation')
        self.row_differentiator.add_mapping('5', 'Volunteering')

    def test_row_that_doesnt_need_splitting(self):
        test_row = {'Q1': 'answer1', 'Q2': 'answer2'}
        self.assertEqual([test_row], _split_row_into_multiple_responses(test_row, self.row_differentiator))

    def test_row_with_one_split(self):

        test_row = {'Q1': 23, '1_Q2_Something': 'alligators', '2_Q2_Something': 'crocodiles'}
        expected = [
            {'Q1': 'Internship', 'Q2_Something': 'alligators'},
            {'Q1': 'Research', 'Q2_Something': 'crocodiles'}
        ]
        self.assertEqual(expected, _split_row_into_multiple_responses(test_row, self.row_differentiator))

    def test_row_with_multiple_splits(self):
        test_row = {'Q1': 23, '1_Q2_Something': 'alligators', '2_Q2_Something': 'crocodiles',
                    '3_Q2_Something': 'lizards', '4_Q2_Something': 'dragons'}
        expected = [
            {'Q1': 'Internship', 'Q2_Something': 'alligators'},
            {'Q1': 'Research', 'Q2_Something': 'crocodiles'},
            {'Q1': 'Fellowship', 'Q2_Something': 'lizards'},
            {'Q1': 'Vacation', 'Q2_Something': 'dragons'}
        ]
        self.assertEqual(expected, _split_row_into_multiple_responses(test_row, self.row_differentiator))

    def test_only_splits_rows_with_non_null_responses(self):
        test_row = {'Q1': 23, '1_Q2_Something': 'alligators', '1_Q3': 'chickens',
                    '2_Q2_Something': '', '2_Q3': '',
                    '3_Q2_Something': 'crocodiles', '3_Q3': 'roosters',
                    '4_Q2_Something': '', '4_Q3': '',
                    '5_Q2_Something': '', '5_Q3': 'hens'}
        expected = [
            {'Q1': 'Internship', 'Q2_Something': 'alligators', 'Q3': 'chickens'},
            {'Q1': 'Fellowship', 'Q2_Something': 'crocodiles', 'Q3': 'roosters'},
            {'Q1': 'Volunteering', 'Q2_Something': '', 'Q3': 'hens'}
        ]
        self.assertEqual(expected, _split_row_into_multiple_responses(test_row, self.row_differentiator))

    def test_row_with_no_multi_question_responses(self):
        test_row = {'Q1': 23, '1_Q2_Something': '', '1_Q3': '',
                    '2_Q2_Something': '', '2_Q3': '',
                    '3_Q2_Something': '', '3_Q3': '',
                    '4_Q2_Something': '', '4_Q3': '',
                    '5_Q2_Something': '', '5_Q3': '', 'Q4': 'forty-two'}
        expected = [{'Q1': 'Internship', 'Q2_Something': '', 'Q3': '', 'Q4': 'forty-two'}]
        self.assertEqual(expected, _split_row_into_multiple_responses(test_row, self.row_differentiator))

    def test_split_multiple_rows(self):
        test_rows = [
            {'Q1': 23,
             '1_Q2_Something': 'alligators', '1_Q3': 'chickens',
             '2_Q2_Something': '', '2_Q3': '',
             '3_Q2_Something': 'crocodiles', '3_Q3': 'roosters',
             '4_Q2_Something': '', '4_Q3': '',
             '5_Q2_Something': '', '5_Q3': 'hens'},
            {'Q1': 98,
             '1_Q2_Something': '', '1_Q3': '',
             '2_Q2_Something': '', '2_Q3': '',
             '3_Q2_Something': 'dragons', '3_Q3': 'hawks',
             '4_Q2_Something': 'bearded dragons', '4_Q3': '',
             '5_Q2_Something': '', '5_Q3': ''},
            {'Q1': 2135,
             '1_Q2_Something': '', '1_Q3': '',
             '2_Q2_Something': 'Octapus', '2_Q3': 'Carrot',
             '3_Q2_Something': '', '3_Q3': '',
             '4_Q2_Something': '', '4_Q3': '',
             '5_Q2_Something': '', '5_Q3': ''}
        ]
        expected = [
            {'Q1': 'Internship', 'Q2_Something': 'alligators', 'Q3': 'chickens'},
            {'Q1': 'Fellowship', 'Q2_Something': 'crocodiles', 'Q3': 'roosters'},
            {'Q1': 'Volunteering', 'Q2_Something': '', 'Q3': 'hens'},
            {'Q1': 'Fellowship', 'Q2_Something': 'dragons', 'Q3': 'hawks'},
            {'Q1': 'Vacation', 'Q2_Something': 'bearded dragons', 'Q3': ''},
            {'Q1': 'Research', 'Q2_Something': 'Octapus', 'Q3': 'Carrot'},
        ]
        self.assertEqual(expected, split_response_rows(test_rows, self.row_differentiator))

    def test_split_response_rows_throws_error_if_not_all_rows_have_the_same_keys(self):
        test_rows = [
            {'a': 1, 'b': 2},
            {'a': 84, 'c': 12}
        ]
        with self.assertRaises(ValueError):
            split_response_rows(test_rows, self.row_differentiator)