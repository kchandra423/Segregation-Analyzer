import json
import os
from pprint import pprint

from census import Census
from dotenv import load_dotenv
POPULATION = 'B02001_001E'
HISPANIC = 'B03002_012E'
BLACK_HISPANIC = 'B03002_014E'
BLACK = 'B02001_003E'

# black +  hispanic - black and hispanic
# black or hispanic

load_dotenv()
KEY = os.getenv('API_KEY')
c = Census(KEY)


def clean_data(raw: dict):
    raw['BROWN'] = get_brown(raw)
    raw['POP'] = raw.pop(POPULATION)
    del raw[BLACK]
    del raw[HISPANIC]
    del raw[BLACK_HISPANIC]


def clean_all_data(raw: list):
    for point in raw:
        clean_data(point)


def get_brown(json: dict):
    return json[HISPANIC] + json[BLACK] - json[BLACK_HISPANIC]


def process_state(state):
    raw = c.acs5.state_county(('NAME', BLACK, HISPANIC, BLACK_HISPANIC, POPULATION),
                              state['state'], Census.ALL)
    clean_all_data(raw)
    state["Counties"] = raw

    for county in state['Counties']:
        raw_blocks = c.acs5.state_county_blockgroup(
            (BLACK, HISPANIC, BLACK_HISPANIC, POPULATION), county['state'], county['county'],
            Census.ALL)
        clean_all_data(raw_blocks)
        county['Blocks'] = raw_blocks
    with open(f"newDataSets/{state['NAME']}.json", "w") as outfile:
        json.dump(state, outfile)
    pprint(state)


def ok():
    data = c.acs5.us(('NAME', BLACK, HISPANIC, BLACK_HISPANIC, POPULATION))[0]
    clean_data(data)
    raw = c.acs5.state(('NAME', BLACK, HISPANIC, BLACK_HISPANIC, POPULATION), Census.ALL)
    clean_all_data(raw)
    data['States'] = raw
    with open(f"newDataSets/America.json", "w") as outfile:
        json.dump(data, outfile)
    for state in data['States']:
        process_state(state)
