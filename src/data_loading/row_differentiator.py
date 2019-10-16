class RowDifferentiator:

    def __init__(self, differentiator_field: str):
        self._field = differentiator_field
        self._mapping = {}

    @property
    def field_name(self) -> str:
        return self._field

    def add_mapping(self, grouping_id: str, value: str):
        self._mapping[grouping_id] = value

    def get_mapping_for_id(self, grouping_id: str) -> str:
        return self._mapping[grouping_id]