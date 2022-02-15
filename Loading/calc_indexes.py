import json
from math import log

import Loading


def export(data, name: str):
    with open(f'data/{name}.json', 'w') as fp:
        json.dump(data, fp)


def rank(areas):
    areas = sorted(areas, key=lambda x: x['Divergence'])
    for rank, area in enumerate(areas, 1):
        area['Divergence Rank'] = rank

    areas = sorted(areas, key=lambda x: x['Isolation'])
    for rank, area in enumerate(areas, 1):
        area['Isolation Rank'] = rank
        area['Rank sum'] = area['Isolation Rank'] + area['Divergence Rank']

    areas = sorted(areas, key=lambda x: x['Rank sum'])
    for rank, area in enumerate(areas, 1):
        area['Rank'] = rank
        del area['Rank sum']


# def calc_chi_us(america: dict):
#     america['Chi2'] = calc_chi(america)
#     for state in america['Sub_Areas']:
#         state['Chi2'] = calc_chi(state)
#         for county in state['Sub_Areas']:
#             county['Chi2'] = calc_chi(county)
#
#
# def calc_chi(area):
#     if not area['Valid']:
#         return
#     value = calc_chi_recursive(area, area['BROWN'] / area['POP'])
#
#     datapoints = value[1]
#     chi = value[0]
#     p = chi2.cdf(chi, datapoints - 1)
#     Loading.chi_distribution.append(p)
#     return p


# def calc_chi_recursive(area, proportion):
#     if is_lowest_level(area):
#         return calc_chi_contribution(area, proportion), 1
#     chi_contribution = 0
#     datapoints = 0
#     for sub_area in area['Sub_Areas']:
#         value = calc_chi_recursive(sub_area, proportion)
#         chi_contribution += value[0]
#         datapoints += value[1]
#     return chi_contribution, datapoints
#
#
# def calc_chi_contribution(area, proportion):
#     expected = proportion * area['POP']
#     if expected == 0:
#         return 0
#     return pow(area['BROWN'] - expected, 2) / expected


def calc_iso_us(america: dict):
    america['Isolation'] = calc_iso(america)
    for state in america['Sub_Areas']:
        state['Isolation'] = calc_iso(state)
        for county in state['Sub_Areas']:
            county['Isolation'] = calc_iso(county)


def calc_div_us(america: dict):
    america['Divergence'] = calc_divergence(america)


def calc_div_districts(districts):
    for district in districts:
        district['Divergence'] = calc_divergence(district)


def calc_iso_districts(districts):
    for district in districts:
        district['Isolation'] = calc_iso(district)


def split(america):
    states = []
    counties = []
    tracts = []
    for state in america['Sub_Areas']:
        for county in state['Sub_Areas']:
            for tract in county['Sub_Areas']:
                tracts.append(tract)
            county.pop('Sub_Areas')
            counties.append(county)
        state.pop('Sub_Areas')
        states.append(state)
    america.pop('Sub_Areas')
    return america, states, counties, tracts


def find_state(states, fip):
    for state in states:
        if state['state'] == fip:
            return state


def find_county(counties, fip):
    for county in counties:
        if county['county'] == fip:
            return county


def rerank_america(america, states, counties):
    for state in states:
        america_state = find_state(america['Sub_Areas'], state['state'])
        america_state['Rank'] = state['Rank']
        america_state['Divergence Rank'] = state['Divergence Rank']
        america_state['Isolation Rank'] = state['Isolation Rank']
    for county in counties:
        america_state = find_state(america['Sub_Areas'], county['state'])
        america_county = find_county(america_state['Sub_Areas'], county['county'])
        america_county['Rank'] = county['Rank']
        america_county['Divergence Rank'] = county['Divergence Rank']
        america_county['Isolation Rank'] = county['Isolation Rank']


def calc_iso_contribution(sub_area, area):
    pop = sub_area['POP']
    brown = sub_area['BROWN']
    brown_tot = area['BROWN']
    return ((brown / (brown_tot if brown_tot > 0 else 1)) * (
        brown / pop if pop > 0 else 1))


def calc_iso(area):
    if not area['Valid']:
        return 0
    iso = calc_iso_recur(area, area)
    p = area['BROWN'] / area['POP']
    value = abs(iso - p)
    Loading.iso_distribution.append(value)

    return value


def calc_iso_recur(area, super_area):
    if is_lowest_level(area):
        return calc_iso_contribution(area, super_area)
    iso_contribution = 0
    for sub_area in area['Sub_Areas']:
        iso_contribution += calc_iso_recur(sub_area, super_area)
    return iso_contribution


# def calc_div_direct(county: dict):
#     div = 0
#     for tract in county['Sub_Areas']:
#         for block in tract['Sub_Areas']:
#             pop_proportion = block['POP'] / county['POP']
#             div += pop_proportion * calc_iso_contribution(block, county)
#     return div


def calc_divergence(area: dict):
    if not area['Valid']:
        return
    return calc_divergence_recur(area, None)


def calc_divergence_recur(area: dict, super_area):
    if is_lowest_level(area):
        return calc_divergence_contribution(area, super_area)
    inter_div = 0
    for sub_area in area['Sub_Areas']:
        local_pop_proportion = sub_area['POP'] / area['POP']
        sub_area['Divergence'] = calc_divergence_recur(sub_area, area)
        inter_div += local_pop_proportion * sub_area['Divergence']
    between_div = calc_between_divergence(area)
    value = inter_div + between_div
    # if area['Valid']:
    #     Loading.div_distribution.append(value)
    return value


def calc_between_divergence(area):
    div = 0
    sub_areas = area['Sub_Areas']
    for sub_area in sub_areas:
        local_pop_proportion = sub_area['POP'] / area['POP']
        div += local_pop_proportion * calc_divergence_contribution(sub_area, area)
    return div


def calc_divergence_contribution(sub_area, area):
    pop = sub_area['POP']
    if area is None:
        return
    pop_tot = area['POP']
    if pop == 0:
        pop = 1

    brown_proportion = sub_area['BROWN'] / pop
    brown_proportion_tot = area['BROWN'] / pop_tot

    non_brown_proportion = get_non_brown(sub_area) / pop
    non_brown_proportion_tot = get_non_brown(area) / pop_tot

    brown_div = 1
    if brown_proportion != 0 and brown_proportion_tot != 0:
        brown_div = brown_proportion * log(brown_proportion / brown_proportion_tot, 2)
    non_brown_div = 1
    if non_brown_proportion != 0 and non_brown_proportion_tot != 0:
        non_brown_div = non_brown_proportion * log(non_brown_proportion / non_brown_proportion_tot, 2)

    return min(brown_div + non_brown_div, 1)


def get_non_brown(area):
    return area['POP'] - area['BROWN']


def is_lowest_level(area):
    return 'Sub_Areas' not in area.keys()
