import json
import os
from pprint import pprint
from joblib import Parallel, delayed

POPULATION = 'B02001_001E'
WHITE = 'B02001_002E'
BLACK = 'B02001_003E'
NATIVE = 'B02001_004E'
ASIAN = 'B02001_005E'
PACIFIC_ISLANDER = 'B02001_005E'

from census import Census
from dotenv import load_dotenv
from jsonschema import validate

load_dotenv()
KEY = os.getenv('API_KEY')
c = Census(KEY)
data = c.acs5.state(('NAME', WHITE, BLACK, NATIVE, ASIAN, PACIFIC_ISLANDER, POPULATION), Census.ALL)

# # state
# schema = {
#     "type": "object",
#     "properties": {
#         "price": {"type": "number"},
#         "name": {"type": "string"},
#     },
# }


# validate(instance={"name": "Eggs", "price": 34.99}, schema=schema)

num_done = 0


def process_state(state):
    state["Counties"] = c.acs5.state_county(('NAME', WHITE, BLACK, NATIVE, ASIAN, PACIFIC_ISLANDER, POPULATION),
                                            state['state'], Census.ALL)

    for county in state['Counties']:
        county['Blocks'] = c.acs5.state_county_blockgroup(
            ('NAME', WHITE, BLACK, NATIVE, ASIAN, PACIFIC_ISLANDER, POPULATION), county['state'], county['county'],
            Census.ALL)
    with open(f"dataSets/{state['NAME']}.json", "w") as outfile:
        json.dump(state, outfile)
    pprint(state)


def ok():
    Parallel(n_jobs=12)(delayed(process_state)(state) for state in data)
