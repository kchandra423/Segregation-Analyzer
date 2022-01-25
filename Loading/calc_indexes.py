import json
from math import log


def update_contributions(data, contributions):
    for i in range(len(data)):
        data[i]['Dissimilarity Contribution'] = contributions[i][0]

        data[i]['Isolation Contribution'] = contributions[i][1]


def update_indexes(data: dict, dis, iso):
    data['Dissimilarity'] = dis
    data['Isolation'] = iso


def export(data, name: str):
    with open(f'data/{name}.json', 'w') as fp:
        json.dump(data, fp)


def calc_us():
    f = open('data/America.json', 'r')
    america = json.load(f)
    america_dis = 0
    america_iso = 0
    contributions = []
    brown = america['BROWN']
    non_brown = america["POP"] - brown
    for state in america['States']:
        results = calculate_state(state, us_info=(brown, non_brown))
        contributions.append([results[0], results[1]])

        america_dis += results[0]
        america_iso += results[1]
    for i in range(len(contributions)):
        contributions[i][0] /= america_dis if america_dis > 0 else 1
        contributions[i][1] /= america_iso if america_iso > 0 else 1

    update_contributions(america['States'], contributions)
    update_indexes(america, america_dis, america_iso)
    export(america, "America_indexed")


def calculate_state(state: dict, us_info):
    state_dis = 0
    state_iso = 0
    us_dis_contribution = 0
    us_iso_contribution = 0
    contributions = []
    brown = state['BROWN']
    non_brown = state['POP'] - brown
    for county in state['Counties']:
        results = calculate_county(county, (brown, non_brown), us_info)

        contributions.append([results[0], results[1]])
        us_dis_contribution += results[2]
        us_iso_contribution += results[3]
        state_dis += results[0]
        state_iso += results[1]

    for i in range(len(contributions)):
        contributions[i][0] /= state_dis if state_dis > 0 else 1

        contributions[i][1] /= state_iso if state_iso > 0 else 1
    update_contributions(state['Counties'], contributions)
    update_indexes(state, state_dis, state_iso)
    print(f'Finished {state["NAME"]}')

    return us_dis_contribution, us_iso_contribution


def calculate_county(county: dict, state_info, us_info):
    state_dis_contribution = 0
    state_iso_contribution = 0
    us_dis_contribution = 0
    us_iso_contribution = 0
    brown_county = county['BROWN']
    non_brown_county = county['POP'] - brown_county
    contributions = []
    county_dis = 0
    county_iso = 0
    for tract in county['Tracts']:
        results = calculate_tract(tract, (brown_county, non_brown_county), state_info, us_info)
        contributions.append([results[0], results[1]])

        county_dis += results[0]
        county_iso += results[1]
        state_dis_contribution += results[2]
        state_iso_contribution += results[3]
        us_dis_contribution += results[4]
        us_iso_contribution += results[5]
    for i in range(len(contributions)):
        contributions[i][0] /= county_dis if county_dis > 0 else 1
        contributions[i][1] /= county_iso if county_iso > 0 else 1
    update_contributions(county['Tracts'], contributions)
    update_indexes(county, county_dis, county_iso)
    print(f'Finished {county["NAME"]}')
    return state_dis_contribution, state_iso_contribution, us_dis_contribution, us_iso_contribution


def calculate_tract(tract, county_info, state_info, us_info):
    state_dis_contribution = 0
    state_iso_contribution = 0
    us_dis_contribution = 0
    us_iso_contribution = 0
    county_dis_contribution = 0
    county_iso_contribution = 0
    brown_county = county_info[0]
    non_brown_county = county_info[1]
    for block in tract['Blocks']:
        brown = block['BROWN']
        non_brown = block['POP'] - brown
        county_dis_contribution += calc_dis_contribution(brown, brown_county, non_brown, non_brown_county)
        county_iso_contribution += calc_iso_contribution(brown, brown_county, non_brown)
        state_dis_contribution += calc_dis_contribution(brown, state_info[0], non_brown, state_info[1])
        state_iso_contribution += calc_iso_contribution(brown, state_info[0], non_brown)
        us_dis_contribution += calc_dis_contribution(brown, us_info[0], non_brown, us_info[1])
        us_iso_contribution += calc_iso_contribution(brown, us_info[0], non_brown)
    return county_dis_contribution, county_iso_contribution, state_dis_contribution, \
           state_iso_contribution, us_dis_contribution, us_iso_contribution


def calc_div_us():
    f = open('data/America.json', 'r')
    america = json.load(f)
    between_district = 0
    within_district = 0
    for state in america['States']:
        within_district+= calc_div_state()
    export(america, "America_indexed")


def calc_div_state(state, us):


def calc_dis_contribution(brown, brown_tot, non_brown, non_brown_tot):
    return 0.5 * abs(brown / (brown_tot if brown_tot > 0 else 1) - non_brown / (
        non_brown_tot if non_brown_tot > 0 else 1))


def calc_iso_contribution(brown, brown_tot, non_brown):
    pop = brown + non_brown
    return (brown / (brown_tot if brown_tot > 0 else 1)) * (
            brown / (pop if pop > 0 else 1))


def calc_divergence(sub_areas, area):
    div = 0
    for sub_area in sub_areas:
        local_pop_proportion = sub_area['POP'] / area['POP']
        div += local_pop_proportion * calc_divergence_contribution(sub_area['BROWN'], area['BROWN'],
                                                                   get_non_brown(sub_area),
                                                                   get_non_brown(area))
    return div


def get_non_brown(area):
    return area['POP'] - area['BROWN']


def calc_divergence_contribution(brown, brown_tot, non_brown, non_brown_tot):
    brown_proportion = brown / (brown + non_brown)
    brown_proportion_tot = brown_tot / (brown_tot + non_brown_tot)
    brown_proportion_tot = brown_proportion_tot if brown_proportion_tot > 0 else 1
    return brown_proportion * log(brown_proportion_tot / brown_proportion_tot, 2)
