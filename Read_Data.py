import json

from Load_Data import BLACK, WHITE


def thing():
    data: list
    with open('Californiat.json', 'r') as f:
        data = json.load(f)
    print(f'Dissimilarity index for Cali is : {calculate_dissimilarity(data)}')
    for county in data:
        print(f'Dissimilarity index for {county["NAME"]} is : {calculate_dissimilarity(county["Tracts"])}')


def calculate_dissimilarity(data: list) -> int:
    black_total = 0
    white_total = 0
    for sub_level in data:
        black_total += sub_level[BLACK]
        white_total += sub_level[WHITE]
    index = 0
    for sub_level in data:
        index += abs(sub_level[WHITE] / white_total - sub_level[BLACK] / black_total)
    return int(index * 0.5 * 100)
