import pprint

from census import Census

from Loading import BLACK, POPULATION, HISPANIC, BLACK_HISPANIC, db, c


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


def process_county(county: dict):
    clean_data(county)
    raw_blocks = c.acs5.state_county_blockgroup(
        (BLACK, HISPANIC, BLACK_HISPANIC, POPULATION), county['state'], county['county'],
        Census.ALL)
    clean_all_data(raw_blocks)
    county['Blocks'] = export_many(raw_blocks, "Block Groups")
    return county["NAME"], export(county, 'Counties')


def process_state(state: dict):
    clean_data(state)
    raw_counties = c.acs5.state_county(('NAME', BLACK, HISPANIC, BLACK_HISPANIC, POPULATION),
                                       state['state'], Census.ALL)
    county_ids = []
    for county in raw_counties:
        county_ids.append(process_county(county))

    state["Counties"] = {}
    state["Counties"].update(county_ids)
    pprint.pprint(state)
    return state["NAME"], export(state, "States")


def load_racial_data():
    data = c.acs5.us(('NAME', BLACK, HISPANIC, BLACK_HISPANIC, POPULATION))[0]
    clean_data(data)
    raw = c.acs5.state(('NAME', BLACK, HISPANIC, BLACK_HISPANIC, POPULATION), Census.ALL)
    state_ids = []
    for state in raw:
        state_ids.append(process_state(state))

    data['States'] = {}
    data['States'].update(state_ids)
    export(data, "United States")


def export(json: dict, lvl: str):
    db.get_collection(lvl).insert_one(json)
    return json["_id"]


def export_many(jsons: list, lvl: str) -> list:
    ids = []
    db.get_collection(lvl).insert_many(jsons)
    for json in jsons:
        ids.append(json['_id'])
    return ids
