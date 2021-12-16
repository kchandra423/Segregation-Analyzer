import json
import random
from pprint import pprint

from Reading.SegregationReport import SegregationReport


def thing(state: str):
    with open(f'newDataSets/{state}.json', 'r') as f:
        data = json.load(f)
    for county in data['Counties']:
        if county['NAME'] == 'Santa Clara County, California':
            choice = county
    # choice = random.choice(list(data['Counties']))
    report = SegregationReport(choice, 'Blocks')
    print(choice['NAME'])
    print(report)
    print(choice['BROWN']/choice['POP'])
