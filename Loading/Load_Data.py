import csv
import json

from census import Census

from Loading import BLACK, POPULATION, HISPANIC, BLACK_HISPANIC, client, c

db = client.get_database('ResidentialData')


# Agency Name,State Name,Agency ID - NCES Assigned,County Number ,ANSI/FIPS State Code ,Web Site URL ,Agency Level
def create_district(district):
    for key in district:
        if district[key] == '†':
            district[key] = None
    district['BROWN'] = 0
    district['POP'] = 0
    district['Valid'] = True
    district['Sub_Areas'] = []


def find_district(districts, _id):
    for district in districts:
        if district['Agency ID'] == _id:
            return district


def open_districts():
    districts = []
    with open('data/Schools/Districts.csv') as district_f:
        district_reader = csv.DictReader(district_f)
        for row in district_reader:
            create_district(row)
            districts.append(row)
    with open('data/Schools/Schools.csv') as school_f:
        school_reader = csv.DictReader(school_f)
        for school in school_reader:
            for key in school:
                if school[key] == '†':
                    school[key] = None
            district = find_district(districts, school['Agency ID'])
            if district is None or school['HISPANIC'] is None or school['BLACK'] is None or school['POP'] is None or \
                    school['POP'] == 0:
                school['Valid'] = False
                continue
            school['Valid'] = True
            school['BROWN'] = int(school.pop('HISPANIC')) + int(school.pop('BLACK'))
            school['POP'] = int(school['POP'])
            district['BROWN'] += school['BROWN']
            district['POP'] += school['POP']
            district['Sub_Areas'].append(school)
    for district in districts:
        if len(district['Sub_Areas']) < 2 or district['POP'] == 0:
            district['Valid'] = False

    with open(f'data/Schools/Districts.json', 'w') as fp:
        json.dump(districts, fp)


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
