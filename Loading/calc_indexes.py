import json
from math import log, sqrt
from statistics import NormalDist

import Loading


def export(data, name: str):
    with open(f'data/{name}.json', 'w') as fp:
        json.dump(data, fp)


def calc_iso_us(america: dict):
    america['Isolation'] = calc_iso(america)
    for state in america['Sub_Areas']:
        state['Isolation'] = calc_iso(state)
        for county in state['Sub_Areas']:
            county['Isolation'] = calc_iso(county)


def calc_div_us(america: dict):
    calc_divergence(america)


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

    export(states, 'States')
    export(america, 'United States')
    export(counties, 'Counties')
    export(tracts, 'Tracts')


def calc_iso_contribution(sub_area, area):
    pop = sub_area['POP']
    brown = sub_area['BROWN']
    brown_tot = area['BROWN']
    return ((brown / (brown_tot if brown_tot > 0 else 1)) * (
        brown / pop if pop > 0 else 1))


def calc_iso(area):
    if not area['Valid']:
        return
    iso = calc_iso_recur(area, area)
    p = area['BROWN'] / area['POP']
    if p == 0:
        p = 1
    sx = sqrt(p * (1 - p) / area['BROWN'] if area['BROWN'] > 0 else 1)
    distribution = NormalDist(mu=p, sigma=sx)
    value = distribution.cdf(iso)
    value = abs(value - 0.5) * 2
    Loading.distribution.append(value)
    if value < 0.95 and value != 0:
        Loading.number += 1
        print(f"{area['NAME']} with {value}")

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
    return calc_divergence_recur(area, None)


def calc_divergence_recur(area: dict, super_area):
    if is_lowest_level(area):
        return calc_divergence_contribution(area, super_area)
    inter_div = 0
    if area['POP'] == 0:
        return 0
    for sub_area in area['Sub_Areas']:
        local_pop_proportion = sub_area['POP'] / area['POP']
        sub_area['Divergence'] = calc_divergence_recur(sub_area, area)
        inter_div += local_pop_proportion * sub_area['Divergence']
    between_div = calc_between_divergence(area)
    return inter_div + between_div


def calc_between_divergence(area):
    div = 0
    sub_areas = area['Sub_Areas']
    for sub_area in sub_areas:
        local_pop_proportion = sub_area['POP'] / area['POP']
        div += local_pop_proportion * calc_divergence_contribution(sub_area, area)
    return div


def calc_divergence_contribution(sub_area, area):
    pop = sub_area['POP']
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

    return brown_div + non_brown_div


def get_non_brown(area):
    return area['POP'] - area['BROWN']


def is_lowest_level(area):
    return 'Sub_Areas' not in area.keys()
