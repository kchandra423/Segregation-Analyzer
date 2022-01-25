import json
from math import log


# def update_contributions(data, contributions):
#     for i in range(len(data)):
#         data[i]['Dissimilarity Contribution'] = contributions[i][0]
#
#         data[i]['Isolation Contribution'] = contributions[i][1]


# def update_indexes(data: dict, dis, iso):
#     data['Dissimilarity'] = dis
#     data['Isolation'] = iso


def export(data, name: str):
    with open(f'data/{name}.json', 'w') as fp:
        json.dump(data, fp)


def calc_iso_us(america: dict):
    america_iso = 0
    for state in america['States']:
        america_iso += calc_iso_state(state, america)
    america['Isolation'] = america_iso
    return america


def calc_iso_state(state: dict, us: dict):
    state_iso = 0
    us_iso_contribution = 0
    for county in state['Counties']:
        result = calc_iso_county(county, state, us)
        us_iso_contribution += result[1]
        state_iso += result[0]
    state['Isolation'] = state_iso
    print(f'Finished {state["NAME"]}')
    return us_iso_contribution


def calc_iso_county(county: dict, state, us):
    state_iso_contribution = 0
    us_iso_contribution = 0
    county_iso = 0
    for tract in county['Tracts']:
        brown = tract['BROWN']
        non_brown = get_non_brown(tract)
        county_brown = county['BROWN']
        state_brown = state['BROWN']
        us_brown = us['BROWN']
        county_iso += calc_iso_contribution(brown, county_brown, non_brown)
        state_iso_contribution += calc_iso_contribution(brown, state_brown, non_brown)
        us_iso_contribution += calc_iso_contribution(brown, us_brown, non_brown)
    county['Isolation'] = county_iso
    print(f'Finished {county["NAME"]}')
    return state_iso_contribution, us_iso_contribution


# def calculate_tract(tract, county_info, state_info, us_info):
#     state_dis_contribution = 0
#     state_iso_contribution = 0
#     us_dis_contribution = 0
#     us_iso_contribution = 0
#     county_dis_contribution = 0
#     county_iso_contribution = 0
#     brown_county = county_info[0]
#     non_brown_county = county_info[1]
#     for block in tract['Blocks']:
#         brown = block['BROWN']
#         non_brown = block['POP'] - brown
#         county_dis_contribution += calc_dis_contribution(brown, brown_county, non_brown, non_brown_county)
#         county_iso_contribution += calc_iso_contribution(brown, brown_county, non_brown)
#         state_dis_contribution += calc_dis_contribution(brown, state_info[0], non_brown, state_info[1])
#         state_iso_contribution += calc_iso_contribution(brown, state_info[0], non_brown)
#         us_dis_contribution += calc_dis_contribution(brown, us_info[0], non_brown, us_info[1])
#         us_iso_contribution += calc_iso_contribution(brown, us_info[0], non_brown)
#     return county_dis_contribution, county_iso_contribution, state_dis_contribution, \
#            state_iso_contribution, us_dis_contribution, us_iso_contribution


def calc_div_us(america: dict):
    within = 0
    for state in america['States']:
        within += state['POP'] / america['POP'] * calc_div_state(state)
    between = calc_divergence(america['States'], america)
    america['Divergence'] = between + within
    export(america, "America_indexed")


def calc_div_state(state):
    within = 0
    for county in state['Counties']:
        within += county['POP'] / state['POP'] * calc_div_county(county)
    between = calc_divergence(state['Counties'], state)
    div = within + between
    state['Divergence'] = div
    return div


def calc_div_county(county):
    div = calc_divergence(county['Tracts'], county)
    county['Divergence'] = div
    return div


# def calc_dis_contribution(brown, brown_tot, non_brown, non_brown_tot):
#     return 0.5 * abs(brown / (brown_tot if brown_tot > 0 else 1) - non_brown / (
#         non_brown_tot if non_brown_tot > 0 else 1))


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
    pop = brown + non_brown

    brown_proportion = brown / pop
    brown_proportion_tot = brown_tot / pop
    brown_proportion_tot = brown_proportion_tot if brown_proportion_tot > 0 else 1

    non_brown_proportion = non_brown / pop
    non_brown_proportion_tot = non_brown_tot / pop
    non_brown_proportion_tot = non_brown_proportion_tot if non_brown_proportion_tot > 0 else 1

    brown_div = brown_proportion * log(brown_proportion / brown_proportion_tot, 2)
    non_brown_div = non_brown_proportion * log(non_brown_proportion / non_brown_proportion_tot, 2)

    return brown_div + non_brown_div
