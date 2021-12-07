import json
from pprint import pprint

from Loading.Load_Data import BLACK, NATIVE, PACIFIC_ISLANDER, POPULATION


def thing(state: str):
    with open(f'dataSets/{state}.json', 'r') as f:
        data = json.load(f)
    dissimilarity = calculate_dissimilarity(data['Counties'], get_brown_share(data), get_pop(data))
    print(dissimilarity)
    countyinput()


def calculate_dissimilarity(sub_levels: list, brown_total_share: int, total_pop: int) -> int:
    index = 0
    contributions = {}
    totals = total_pop * brown_total_share * (1 - brown_total_share)
    for sub_level in sub_levels:
        contribution = 0.5 * get_pop(sub_level) * ((abs(get_brown_share(sub_level) - brown_total_share)) / totals) * 100
        contributions[sub_level["NAME"]] = contribution
        index += contribution
    index = int(index)
    for sub_level in sub_levels:
        expected = sub_level[POPULATION] / total_pop
        given = contributions[sub_level["NAME"]] / index
        contributions[sub_level["NAME"]] = given/expected *100 -100

    pprint(contributions)
    return index


def get_pop(geo: dict) -> int:
    return geo[POPULATION]


def get_brown_share(geo: dict) -> int:
    return (geo[BLACK] + geo[NATIVE] + geo[PACIFIC_ISLANDER]) / get_pop(geo)
