import csv
import json
# Agency Name,State Name,Agency ID - NCES Assigned,County Number ,ANSI/FIPS State Code ,Web Site URL ,Agency Level
import os

import census
import geojson
import geopandas as gp
import numpy
import us

from Loading import c, HISPANIC, HISPANIC_ADULT, BLACK_NOT_HISPANIC, BLACK_NOT_HISPANIC_ADULT, POPULATION, export


def deal_with_geo_pandas(schools):
    for school in schools:
        if 'low' not in school.keys():
            school['low'] = numpy.nan
        if 'high' not in school.keys():
            school['high'] = numpy.nan


def getinfo_district(state, elemntary, secondary, unified, district_map):
    state_name = str(us.states.lookup(state))
    districts = district_map.get(state_name, None)
    if districts is None:
        print('couldnt find district')
        print(state_name, elemntary, secondary, unified)
        return
    nulls = 0
    chosen_id = ''
    for _id in (elemntary, secondary, unified):
        if _id == '':
            nulls += 1
        else:
            chosen_id = _id
    if nulls != 2:
        print('wait what')
        print(state, elemntary, secondary, unified)
    for district in districts:
        if district['Agency ID'] == state + chosen_id:
            return district

    print('Couldnt find that district')
    print(state, chosen_id)


def normalize_schools(schools):
    for school in schools:
        school['Valid'] = school.get('Valid', False)
        school['NAME'] = school.get('NAME', None)
        school['School ID'] = school.get('School ID', None)
        school['Agency ID'] = school.get('Agency ID', None)
        school['URL'] = school.get('URL', None)
        school['low'] = school.get('low', None)
        school['high'] = school.get('high', None)
        school['level'] = school.get('level', None)
        school['state'] = school.get('state', None)
        school['lat'] = school.get('lat', None)
        school['long'] = school.get('long', None)
        school['POP'] = int(school.get('POP', 0))
        school['BROWN'] = school.get('BROWN')
        del school['Divergence']
    return schools


def add_data_to_geo():
    district_map = {}
    f = open('data/geojson/School_Districts.json', 'r')
    districts = gp.read_file(f)
    print('Finished loading in data')
    num_completed = 0
    num_with_info = 0

    districts.pop('ALAND')
    districts.pop('AWATER')
    # districts.pop('FUNCTSTAT')
    # districts.pop('ELDSLEA')
    districts.pop('GEO_YEAR')
    districts.pop('LSAD')
    districts.pop('MTFCC')
    districts.pop('SDTYP')
    districts.pop('FUNCSTAT')
    districts['high'] = districts.pop('HIGRADE')
    districts['low'] = districts.pop('LOGRADE')
    districts['lat'] = districts.pop('INTPTLAT')
    districts['long'] = districts.pop('INTPTLON')
    districts['state'] = districts.pop('STATEFP')
    districts['elementary'] = districts.pop('ELSDLEA')
    districts['secondary'] = districts.pop('SCSDLEA')
    districts['unified'] = districts.pop('UNSDLEA')
    districts['Schools'] = ''
    districts['Blocks'] = ''
    districts['Divergence Rank'] = numpy.nan
    districts['Isolation Rank'] = numpy.nan
    districts['Segregation Rank'] = numpy.nan
    districts['Valid'] = False
    districts['POP'] = numpy.nan
    districts['Divergence'] = numpy.nan
    districts['Isolation'] = numpy.nan
    districts['AverageSegregation'] = numpy.nan
    districts['BROWN'] = numpy.nan
    districts.pop('SCHOOLYEAR')
    print('removed all the things')
    for state in os.listdir('data/Schools/Districts'):
        if 'ds_store' in state.lower():
            continue
        if '06' not in state:
            continue
        f = open(f'data/Schools/Districts/{state}')
        district_map[state.replace('.json', '')] = json.load(f)
    for idx, district in districts.iterrows():
        num_completed += 1
        info = getinfo_district(district['state'], district['elementary'], district['secondary'], district['unified'],
                                district_map)
        if info is None:
            continue
        if info['Valid']:
            districts.at[idx, 'Divergence Rank'] = info['Divergence Rank']
            districts.at[idx, 'Isolation Rank'] = info['Isolation Rank']
            districts.at[idx, 'Segregation Rank'] = info['Segregation Rank']
        districts.at[idx, 'Valid'] = info['Valid']
        districts.at[idx, 'BROWN'] = info['BROWN']
        districts.at[idx, 'POP'] = info['POP']
        districts.at[idx, 'Divergence'] = info['Divergence']
        districts.at[idx, 'Isolation'] = info['Isolation']
        districts.at[idx, 'AverageSegregation'] = (info['Divergence'] + info['Isolation']) / 2
        districts.at[idx, 'Schools'] = json.dumps(normalize_schools(info['sub']) if not None else [])
        districts.at[idx, 'Blocks'] = json.dumps(info['Blocks'] if not None else [])

        num_with_info += 1
        if num_completed % 100 == 0:
            print(f'Finished {num_completed} and {num_with_info} districts')

        state = districts[districts['state'] == '06']

        string = state.to_json()
        geo = geojson.loads(string)
        with open(f"data/geojson/cleaned_districts/06.json", 'w') as fpo:
            geojson.dump(geo, fpo)
    # for i in range(1, 57):
    #     if len(str(i)) == 1:
    #         i = "0" + str(i)
    #     i = str(i)
    #
    #     if state is None:
    #         continue
    #     if len(state.index) == 0:
    #         continue
    #     del string
    #     print(type(geo))


def clean_district(district):
    for key in district:
        if district[key] == '†':
            district[key] = None
    district['Valid'] = True
    district['NAME'] = district.pop('Agency Name')
    district['STATE'] = district.pop('State Name [District] Latest available year')
    district['Agency ID'] = district.pop('Agency ID - NCES Assigned [District] Latest available year')
    district['COUNTY'] = district.pop('County Name [District] 2019-20')
    district['county'] = district.pop('County Number [District] 2019-20')
    district['state'] = district.pop('ANSI/FIPS State Code [District] Latest available year')
    district['URL'] = district.pop('Web Site URL [District] 2019-20')
    district.pop('State Agency ID [District] 2019-20')


def clean_school(school):
    for key in school:
        if school[key] == '†':
            school[key] = None
    school['Valid'] = True
    school['NAME'] = school.pop('School Name')
    school.pop('State Name [Public School] Latest available year')
    school['School ID'] = school.pop('School ID - NCES Assigned [Public School] Latest available year')
    school['Agency ID'] = school.pop('Agency ID - NCES Assigned [Public School] Latest available year')
    school.pop('County Name [Public School] 2019-20')
    school.pop('County Number [Public School] 2019-20')
    school['URL'] = school.pop('Web Site URL [Public School] 2019-20')
    school['low'] = school.pop('Lowest Grade Offered [Public School] 2019-20')
    school['high'] = school.pop('Highest Grade Offered [Public School] 2019-20')
    school['level'] = school.pop('School Level (SY 2017-18 onward) [Public School] 2019-20')
    school['state'] = school.pop('ANSI/FIPS State Code [Public School] Latest available year')
    school['lat'] = school.pop('Latitude [Public School] 2019-20')
    school['long'] = school.pop('Longitude [Public School] 2019-20')

    # school.pop('State School ID [Public School] 2019-20')
    pop = school.pop('Total Race/Ethnicity [Public School] 2019-20')
    school['POP'] = int(pop) if pop is not None else None
    black = school.pop('Black or African American Students [Public School] 2019-20')
    hispanic = school.pop('Hispanic Students [Public School] 2019-20')
    school['BROWN'] = int(black) + int(hispanic) if black is not None and hispanic is not None else None


def create_district(district):
    clean_district(district)
    for key in district:
        if district[key] == '†':
            district[key] = None
    if len(district['Agency ID']) == 6:
        district['Agency ID'] = '0' + district['Agency ID']
    district['BROWN'] = 0
    district['POP'] = 0
    district['Valid'] = True
    district['sub'] = []


def find_district(districts, _id):
    return districts.get(_id, None)


def open_districts():
    districts = {}
    with open('data/Schools/Districts.csv') as district_f:
        district_reader = csv.DictReader(district_f)
        for row in district_reader:
            create_district(row)
            districts[row['Agency ID']] = row
    with open('data/Schools/Schools.csv') as school_f:
        school_reader = csv.DictReader(school_f)
        for school in school_reader:
            clean_school(school)
            district = find_district(districts, school['Agency ID'])
            if district is None or school['BROWN'] is None or school['POP'] is None or \
                    school['POP'] == 0:
                school['Valid'] = False
                continue
            district['BROWN'] += school['BROWN']
            district['POP'] += school['POP']
            district['sub'].append(school)
    for district in districts.values():
        if len(district['sub']) < 2 or district['POP'] == 0 or school['BROWN'] == 0:
            district['Valid'] = False

    with open(f'data/Schools/Districts.json', 'w') as fp:
        json.dump(list(districts.values()), fp)


def get_blocks(tract, county, state):
    return c.pl.get(('NAME', HISPANIC, HISPANIC_ADULT, BLACK_NOT_HISPANIC, BLACK_NOT_HISPANIC_ADULT, POPULATION),
                    geo={'for': 'block:*',
                         'in': f'state:{state} county:{county} tract:{tract}'})


def clean_data(raw: dict):
    raw['BROWN'] = get_brown_adults(raw)
    raw['BROWN_CHILD'] = get_brown_kids(raw)
    raw['POP'] = raw.pop(POPULATION)
    del raw[BLACK_NOT_HISPANIC]
    del raw[BLACK_NOT_HISPANIC_ADULT]
    del raw[HISPANIC]
    del raw[HISPANIC_ADULT]


def clean_all_data(raw):
    for point in raw:
        clean_data(point)


def get_brown_adults(area: dict):
    return int(area[HISPANIC]) + int(area[BLACK_NOT_HISPANIC])


def get_brown_kids(area: dict):
    return int(area[HISPANIC]) - int(area[HISPANIC_ADULT]) + int(area[BLACK_NOT_HISPANIC]) - int(
        area[BLACK_NOT_HISPANIC_ADULT])


# race, pop, school district id
def get_all_census_blocks():
    states = c.pl.state('NAME', census.ALL)
    for state in states:
        blocks = get_blocks('*', '*', state['state'])
        clean_all_data(blocks)
        for block in blocks:
            validate(block)
        export(blocks, f'Schools/Blocks/{state["NAME"]}')
        print(f'Finished {state["NAME"]}')


def validate(area):
    if area['POP'] == 0 or ('sub' in area.keys() and len(area['sub']) < 2):
        area['Valid'] = False
    else:
        area['Valid'] = True
