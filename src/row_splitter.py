from typing import List
import re


class _CompoundQuestion:

    def __init__(self, group: str, question: str):
        self.group = group
        self.question = question
        self.full_question_str = f'{group}_{question}'


class _QuestionGroup:

    def __init__(self):
        self._questions = []
        self._has_answers = False

    def add_question(self, question: _CompoundQuestion):
        self._questions.append(question)

    @property
    def questions(self) -> List[_CompoundQuestion]:
        return self._questions

    @property
    def has_answers(self) -> bool:
        return self._has_answers

    @has_answers.setter
    def has_answers(self, value: bool):
        self._has_answers = value


class _HeaderClassification:

    def __init__(self):
        self._multi_questions = {}
        self._one_question_group_has_answers = False
        self._single_questions = []

    def add_question_to_multi_group(self, question: _CompoundQuestion):
        if question.group not in self._multi_questions:
            self._multi_questions[question.group] = _QuestionGroup()
        self._multi_questions[question.group].add_question(question)

    def add_single_question(self, question: str):
        self._single_questions.append(question)

    def has_multi_questions(self) -> bool:
        return bool(self._multi_questions)

    def question_group_has_answers(self, group: str) -> bool:
        return self._multi_questions[group].has_answers

    def set_question_group_has_answers(self, group: str, has_answers: bool):
        self._multi_questions[group].has_answers = has_answers

    @property
    def multi_questions(self) -> dict:
        return self._multi_questions

    @property
    def single_questions(self) -> List[str]:
        return self._single_questions

    @property
    def one_question_group_has_answers(self) -> bool:
        return self._one_question_group_has_answers

    @one_question_group_has_answers.setter
    def one_question_group_has_answers(self, value: bool):
        self._one_question_group_has_answers = value


class _HeaderClassificationBuilder:

    def __init__(self, table_row: dict):
        self._row = table_row
        self._header_classification = _HeaderClassification()

    def build(self):
        header = self._row.keys()
        for question in header:
            self._record_question(question)
        return self._header_classification

    def _record_multi_question(self, question: str):
        compound_question = self._parse_compound_question_str(question)
        self._header_classification.add_question_to_multi_group(compound_question)
        if self._row[question] != '':
            self._header_classification.set_question_group_has_answers(compound_question.group, True)
            self._header_classification.one_question_group_has_answers = True

    def _record_question(self, question: str) -> _HeaderClassification:
        try:
            self._record_multi_question(question)
        except AttributeError:
            self._header_classification.add_single_question(question)
        return self._header_classification

    @staticmethod
    def _parse_compound_question_str(question: str) -> _CompoundQuestion:
        pattern_match_result = re.match(r'^(\d+)_(Q\d+.*)$', question)
        return _CompoundQuestion(group = pattern_match_result.groups()[0],
                                 question = pattern_match_result.groups()[1])


class _MultiResponseBuilder:

    def __init__(self, row):
        self._row = row
        self._header_classification = _HeaderClassificationBuilder(row).build()

    def build(self) -> List[dict]:
        if self._header_classification.has_multi_questions():
            return self._create_multiple_responses_from_row()
        else:
            return [self._row]

    def _create_multiple_responses_from_row(self) -> List[dict]:
        if self._header_classification.one_question_group_has_answers:
            return self._create_responses_from_row_with_multi_response_answers()
        else:
            return self._create_response_from_row_with_no_question_group_answers()

    def _create_responses_from_row_with_multi_response_answers(self) -> List[dict]:
        result = []
        for question_group in self._header_classification.multi_questions.values():
            if question_group.has_answers:
                result.append(self._create_multi_response_row(question_group))
        return result

    def _create_response_from_row_with_no_question_group_answers(self) -> List[dict]:
        question_group = self._get_random_question_group()
        new_row = self._create_multi_response_row(question_group)
        return [new_row]

    def _create_multi_response_row(self, question_group: _QuestionGroup) -> dict:
        row = self._create_row_from_single_questions()
        return self._enrich_row_with_question_group(row, self._row, question_group)

    def _create_row_from_single_questions(self) -> dict:
        return {question: self._row[question] for question in self._header_classification.single_questions}

    def _enrich_row_with_question_group(self, row: dict, source_row: dict, question_group: _QuestionGroup) -> dict:
        for question in question_group.questions:
            row[question.question] = source_row[question.full_question_str]
        return row

    def _get_random_question_group(self) -> _QuestionGroup:
        question_groups = list(self._header_classification.multi_questions.keys())
        return self._header_classification.multi_questions[question_groups[0]]


def _split_row_into_multiple_responses(row: dict) -> List[dict]:
    return _MultiResponseBuilder(row).build()

def _all_rows_have_the_same_keys(response_rows: List[dict]) -> bool:
    keys = response_rows[0].keys()
    for row in response_rows:
        if row.keys() != keys:
            return False
    return True

def split_response_rows(response_rows: List[dict]) -> List[dict]:
    result = []
    if not _all_rows_have_the_same_keys(response_rows):
        raise ValueError('All rows must have the same column names')
    else:
        for row in response_rows:
            result += _split_row_into_multiple_responses(row)
        return result
