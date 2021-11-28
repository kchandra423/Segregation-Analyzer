import json
import os
from pprint import pprint

POPULATION = 'B02001_001E'
WHITE = 'B02001_002E'
BLACK = 'B02001_003E'
NATIVE = 'B02001_004E'
ASIAN = 'B02001_005E'
PACIFIC_ISLANDER = 'B02001_005E'
from census import Census
from dotenv import load_dotenv
from us import states


def ok():
    load_dotenv()
    KEY = os.getenv('API_KEY')
    c = Census(KEY)
    data = c.acs5.state_county(('NAME', WHITE, BLACK, NATIVE, ASIAN, PACIFIC_ISLANDER, POPULATION), states.CA.fips,
                               '*')
    for county in data:
        county['Tracts'] = c.acs5.state_county(
            (WHITE, BLACK, NATIVE, ASIAN, PACIFIC_ISLANDER, POPULATION), states.CA.fips, county['county'],
            Census.ALL)
        pprint(county)

    with open("Californiat.json", "w") as outfile:
        json.dump(data, outfile)
