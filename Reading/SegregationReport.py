STATE = 'STATE'
COUNTY = 'COUNTY'
USA = 'US'

class SegregationReport:
    def __init__(self, level, sub_levels):
        self._dis = 0
        self._isol = 0
        self._sub_level_data = {}

