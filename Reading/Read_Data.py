import json
from pprint import pprint


def get_info(name: str):
    f = open('data/America_Indexed.json', 'r')
    america = json.load(f)
    states = america['States']
    for state in states:
        if state['NAME'] == name:
            pprint(state)
            return
