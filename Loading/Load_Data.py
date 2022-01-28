import json
import pprint

from census import Census

from Loading import BLACK, POPULATION, HISPANIC, BLACK_HISPANIC, client, c

db = client.get_database('ResidentialData')


def clean_data(raw: dict):
    raw['BROWN'] = get_brown(raw)
    raw['POP'] = raw.pop(POPULATION)
    del raw[BLACK]
    del raw[HISPANIC]
    del raw[BLACK_HISPANIC]


def clean_all_data(raw):
    for point in raw:
        clean_data(point)


def get_brown(area: dict):
    return area[HISPANIC] + area[BLACK] - area[BLACK_HISPANIC]


def load_racial_data():
    america = c.acs5.us(('NAME', BLACK, HISPANIC, BLACK_HISPANIC, POPULATION))[0]
    clean_data(america)

    states = c.acs5.state(('NAME', BLACK, HISPANIC, BLACK_HISPANIC, POPULATION), Census.ALL)
    clean_all_data(states)
    for state in states:
        counties = c.acs5.state_county(('NAME', BLACK, HISPANIC, BLACK_HISPANIC, POPULATION),
                                       state['state'], Census.ALL)
        clean_all_data(counties)
        for county in counties:
            tracts = c.acs5.state_county_tract((BLACK, HISPANIC, BLACK_HISPANIC, POPULATION), county['state'],
                                               county['county'],
                                               Census.ALL)
            clean_all_data(tracts)
            blocks = c.acs5.state_county_blockgroup((BLACK, HISPANIC, BLACK_HISPANIC, POPULATION), county['state'],
                                                    county['county'], Census.ALL)
            clean_all_data(blocks)
            for tract in tracts:
                tract['Blocks'] = []
            for block in blocks:
                tract = get_tract(tracts, block)
                tract['Blocks'].append(block)
            county['Tracts'] = tracts
            print(f'Finished loading {county["NAME"]}')
            # pprint.pprint(county)
        state['Counties'] = counties
        # print(f'Finished loading {state["NAME"]}')
    for state in states:
        if state['NAME'] == "Puerto Rico":
            states.remove(state)
    america['States'] = states
    export(america, 'America_Blocks')


def export(data, name: str):
    with open(f'data/{name}.json', 'w') as fp:
        json.dump(data, fp)


def get_tract(tracts, block):
    for tract in tracts:
        if tract['tract'] == block['tract'] and tract['county'] == block['county']:
            return tract
