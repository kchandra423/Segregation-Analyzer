from census import Census

from Loading import BLACK, POPULATION, HISPANIC, BLACK_HISPANIC, client, c
db = client.get_database('ResidentialData')

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


def find_tracts(tracts, county):
    ids = []
    for tract in tracts:
        if tract['county'] == county['county'] and tract['state'] == county['state']:
            ids.append(tract['_id'])
    return ids


def find_blocks(blocks, tract):
    ids = []
    for block in blocks:
        if block['tract'] == tract['tract'] and block['county'] == tract['county'] and block['state'] == tract['state']:
            ids.append(block['_id'])
    return ids


def process_state(state: dict):
    clean_data(state)
    raw_counties = c.acs5.state_county(('NAME', BLACK, HISPANIC, BLACK_HISPANIC, POPULATION),
                                       state['state'], Census.ALL)
    raw_tracts = c.acs5.state_county_tract(
        (BLACK, HISPANIC, BLACK_HISPANIC, POPULATION), state['state'], Census.ALL,
        Census.ALL)
    raw_blocks = c.acs5.state_county_blockgroup(
        (BLACK, HISPANIC, BLACK_HISPANIC, POPULATION), state['state'], Census.ALL,
        Census.ALL)
    clean_all_data(raw_tracts)
    clean_all_data(raw_blocks)
    clean_all_data(raw_counties)
    export_many(raw_blocks, "Blocks")
    for tract in raw_tracts:
        tract['Blocks'] = find_blocks(raw_blocks, tract)
    export_many(raw_tracts, "Tracts")
    for county in raw_counties:
        county['Tracts'] = find_tracts(raw_tracts, county)

    state["Counties"] = export_many(raw_counties, "Counties")
    return export(state, "States")


def load_racial_data():
    data = c.acs5.us(('NAME', BLACK, HISPANIC, BLACK_HISPANIC, POPULATION))[0]
    clean_data(data)
    raw = c.acs5.state(('NAME', BLACK, HISPANIC, BLACK_HISPANIC, POPULATION), Census.ALL)
    state_ids = []

    for state in raw:
        state_ids.append(process_state(state))
    data['States'] = state_ids
    export(data, "United States")


def export(json: dict, lvl: str):
    return db.get_collection(lvl).insert_one(json).inserted_id


def export_many(jsons: list, lvl: str):
    return db.get_collection(lvl).insert_many(jsons).inserted_ids
