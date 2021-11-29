import json

from Load_Data import BLACK, NATIVE, PACIFIC_ISLANDER, POPULATION


def thing(state: str):
    with open(f'dataSets/{state}.json', 'r') as f:
        data = json.load(f)
    print(calculate_dissimilarity(data['Counties'], get_brown_share(data), get_pop(data)))


def calculate_dissimilarity(sub_levels: list, brown_total_share: int, total_pop: int):
    index = 0
    totals = total_pop * brown_total_share * (1 - brown_total_share)
    for sub_level in sub_levels:
        index += get_pop(sub_level) * ((abs(get_brown_share(sub_level) - brown_total_share)) / totals)

    return int(index * 0.5 * 100)


def get_pop(geo: dict) -> int:
    return geo[POPULATION]


def get_brown_share(geo: dict) -> int:
    return (geo[BLACK] + geo[NATIVE] + geo[PACIFIC_ISLANDER]) / get_pop(geo)
