import pprint

STATE = 'STATE'
COUNTY = 'COUNTY'
USA = 'US'


class SegregationReport:

    def __init__(self, json: dict, sub_levels: str):
        self._dis = 0
        self._isol = 0
        self._sub_level_data = {}
        self.calc(json, sub_levels)

    def calc(self, json: dict, sub_levels: str):
        brown_tot = json['BROWN']
        non_brown_tot = json['POP'] - brown_tot
        for sub_level in json[sub_levels]:
            brown = sub_level['BROWN']
            non_brown = sub_level['POP'] - brown
            iso_contribution = (brown / (brown_tot if brown_tot > 0 else 1)) * (
                        brown / (sub_level['POP'] if sub_level['POP'] > 0 else 1))
            dis_contribution = 0.5 * abs(
                brown / (brown_tot if brown_tot > 0 else 1) - non_brown / (non_brown_tot if non_brown_tot > 0 else 1))
            self._sub_level_data[sub_level.get("NAME", sub_level['block group'])] = [dis_contribution, iso_contribution]
            self._dis += dis_contribution
            self._isol += iso_contribution
        for sub_level in json[sub_levels]:
            self._sub_level_data[sub_level.get("NAME", sub_level['block group'])][0] /= self._dis
            self._sub_level_data[sub_level.get("NAME", sub_level['block group'])][1] /= self._isol

    def __str__(self):
        return f"Dissimilarity index: {self._dis}\n" \
               f"Isolation index: {self._isol}\n" \
               f"SCIS: {pprint.pformat(self._sub_level_data)}"
