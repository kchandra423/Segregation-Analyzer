from census import Census

from Loading import HISPANIC, BLACK_NOT_HISPANIC, c, POPULATION
from Loading import export


def clean_data(raw: dict):
    raw['BROWN'] = get_brown_adults(raw)
    # raw['BROWN_CHILD'] = get_brown_kids(raw)
    raw['POP'] = raw.pop(POPULATION)
    del raw[BLACK_NOT_HISPANIC]
    # del raw[BLACK_NOT_HISPANIC_ADULT]
    del raw[HISPANIC]
    # del raw[HISPANIC_ADULT]


def clean_all_data(raw):
    for point in raw:
        clean_data(point)


def get_brown_adults(area: dict):
    return int(area[HISPANIC]) + int(area[BLACK_NOT_HISPANIC])


# def get_brown_kids(area: dict):
#     return int(area[HISPANIC]) - int(area[HISPANIC_ADULT]) + int(area[BLACK_NOT_HISPANIC]) - int(
#         area[BLACK_NOT_HISPANIC_ADULT])


def load_racial_data():
    america = c.pl.us(('NAME', HISPANIC, BLACK_NOT_HISPANIC, POPULATION))[0]
    clean_data(america)

    states = c.pl.state(('NAME', HISPANIC, BLACK_NOT_HISPANIC, POPULATION),
                        Census.ALL)
    clean_all_data(states)
    for state in states:
        counties = c.pl.state_county(
            ('NAME', HISPANIC, BLACK_NOT_HISPANIC, POPULATION),
            state['state'], Census.ALL)
        tracts = c.pl.state_county_tract(
            ('NAME', HISPANIC, BLACK_NOT_HISPANIC, POPULATION),
            state['state'],
            Census.ALL,
            Census.ALL)
        clean_all_data(counties)
        clean_all_data(tracts)
        validate(state)
        for county in counties:
            county['sub'] = []
            for tract in tracts:
                if tract['county'] == county['county'] and tract['state'] == county['state']:
                    county['sub'].append(tract)
                validate(tract)
            validate(county)
        state['sub'] = counties
        validate(state)
        print(f'Finished loading {state["NAME"]}')
    for state in states:
        if state['NAME'] == "Puerto Rico":
            states.remove(state)
    america['sub'] = states
    validate(america)
    export(america, 'tracts/America')


def validate(area):
    if area['POP'] == 0 or ('sub' in area.keys() and len(area['sub']) < 2):
        area['Valid'] = False
    else:
        area['Valid'] = True
# def get_blocks(tract, county, state):
#     return c.pl.get(('NAME', HISPANIC, HISPANIC_ADULT, BLACK_NOT_HISPANIC, BLACK_NOT_HISPANIC_ADULT, POPULATION),
#                     geo={'for': 'block:*',
#                          'in': f'state:{state} county:{county} tract:{tract}'})
