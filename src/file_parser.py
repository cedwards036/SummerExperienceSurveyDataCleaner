from typing import List
from collections import defaultdict

def parse_survey_file(filepath: str) -> List[dict]:

    def _skip_subheader_rows(file):
        NUMBER_OF_SUBHEADER_ROWS = 2
        for i in range(NUMBER_OF_SUBHEADER_ROWS):
            file.readline()

    def _skip_survey_preview_rows(file):
        last_row_read = file.tell()
        current_row = _parse_line_into_list_of_str(file.readline())
        while current_row[2] == 'Survey Preview':
            last_row_read = file.tell()
            current_row = _parse_line_into_list_of_str(file.readline())
        file.seek(last_row_read)

    result = []
    with open(filepath, encoding='utf-8') as file:
        header = parse_header(file)
        _skip_subheader_rows(file)
        _skip_survey_preview_rows(file)
        for line in file:
            row = dict(zip(header, _parse_line_into_list_of_str(line)))
            result.append(row)
    return result


def parse_header(file) -> List[str]:

    def _add_quantifiers_to_repeated_header_labels(header: List[str]) -> List[str]:
        header_field_counts = defaultdict(int)
        for i, header_field in enumerate(header):
            header_field_counts[header_field] += 1
            if header_field_counts[header_field] > 1:
                header[i] = f'{header[i]}_{header_field_counts[header_field]}'
        return header

    header = _parse_line_into_list_of_str(file.readline())
    return _add_quantifiers_to_repeated_header_labels(header)

def _parse_line_into_list_of_str(line: str) -> List[str]:
    return line.strip().split(',')
