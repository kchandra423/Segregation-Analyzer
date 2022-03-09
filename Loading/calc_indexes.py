import json
from math import log

import Loading


def export(data, name: str):
    with open(f'data/{name}.json', 'w') as fp:
        json.dump(data, fp)


def resident_rank(areas):
    valids = len(list(filter(lambda x: x['Valid'], areas)))
    areas = sorted(filter(lambda x: x['Valid'], areas), key=lambda x: x['Residential Divergence'])
    for rank, area in enumerate(areas, 1):
        area['Residential Divergence Rank'] = rank / valids

    areas = sorted(filter(lambda x: x['Valid'], areas), key=lambda x: x['Residential Isolation'])
    for rank, area in enumerate(areas, 1):
        area['Residential Isolation Rank'] = rank / valids
        area['Residential Rank sum'] = area['Isolation Rank'] + area['Residential Divergence Rank']

    areas = sorted(filter(lambda x: x['Valid'], areas), key=lambda x: x['Residential Rank sum'])
    for rank, area in enumerate(areas, 1):
        area['Residential Segregation Rank'] = rank / valids
        del area['Rank sum']
def rank(areas):
    valids = len(list(filter(lambda x: x['Valid'], areas)))
    areas = sorted(filter(lambda x: x['Valid'], areas), key=lambda x: x['Residential Divergence'])
    for rank, area in enumerate(areas, 1):
        area['Residential Divergence Rank'] = rank / valids

    areas = sorted(filter(lambda x: x['Valid'], areas), key=lambda x: x['Residential Isolation'])
    for rank, area in enumerate(areas, 1):
        area['Residential Isolation Rank'] = rank / valids
        area['Residential Rank sum'] = area['Residential Isolation Rank'] + area['Residential Divergence Rank']

    areas = sorted(filter(lambda x: x['Valid'], areas), key=lambda x: x['Residential Rank sum'])
    for rank, area in enumerate(areas, 1):
        area['Residential Segregation Rank'] = rank / valids
        del area['Residential Rank sum']


def rerank_america(america, states, counties):
    for state in states:
        if not state['Valid']:
            continue
        america_state = find_state(america['sub'], state['state'])
        america_state['Segregation Rank'] = state['Segregation Rank']
        america_state['Divergence Rank'] = state['Divergence Rank']
        america_state['Isolation Rank'] = state['Isolation Rank']
    for county in counties:
        if not county['Valid']:
            continue
        america_state = find_state(america['sub'], county['state'])
        america_county = find_county(america_state['sub'], county['county'])
        america_county['Segregation Rank'] = county['Segregation Rank']
        america_county['Divergence Rank'] = county['Divergence Rank']
        america_county['Isolation Rank'] = county['Isolation Rank']


def calc_iso_us(america: dict):
    america['Isolation'] = calc_iso(america)
    for state in america['sub']:

        state['Isolation'] = calc_iso(state)
        for county in state['sub']:
            county['Isolation'] = calc_iso(county)


def calc_list_seg(blocks):
    brown_tot = 0
    pop_tot = 0
    for block in blocks:
        brown_tot += block[0]
        pop_tot += block[1]

    non_brown_tot = pop_tot - brown_tot
    divergence = calc_list_divergence(blocks, brown_tot, non_brown_tot, pop_tot)
    isolation = calc_list_iso(blocks, brown_tot)
    value = abs(isolation - (brown_tot / pop_tot))
    return 2 * divergence, value


def calc_list_iso(blocks, brown_tot):
    iso = 0
    for block in blocks:
        t1 = 0 if block[0] == 0 else block[0] / brown_tot
        t2 = 0 if block[1] == 0 else block[0] / block[1]
        iso += t1 * t2
    return iso


def calc_list_divergence(blocks, brown_tot, non_brown_tot, pop_tot):
    div = 0

    brown_proportion_tot = brown_tot / pop_tot

    non_brown_proportion_tot = non_brown_tot / pop_tot
    for block in blocks:
        brown_proportion = block[0] / block[1]
        non_brown = block[1] - block[0]
        non_brown_proportion = non_brown / block[1]

        brown_div = 0
        if brown_proportion != 0 and brown_proportion_tot != 0:
            brown_div = brown_proportion * log(brown_proportion / brown_proportion_tot, 2)
        non_brown_div = 0
        if non_brown_proportion != 0 and non_brown_proportion_tot != 0:
            non_brown_div = non_brown_proportion * log(non_brown_proportion / non_brown_proportion_tot, 2)
        div += (block[1] / pop_tot) * (brown_div + non_brown_div)
    return div


def calc_div_us(america: dict):
    america['Divergence'] = calc_divergence(america)


def calc_resident_divergence(area: dict):
    return calc_resident_divergence_recur(area, None)


def calc_resident_divergence_recur(area: dict, super_area):
    if is_lowest_level(area):
        return calc_divergence_contribution(area, super_area)
    inter_div = 0
    for sub_area in area['Blocks']:
        local_pop_proportion = sub_area['POP'] / area['POP']
        sub_area['Residential Divergence'] = calc_resident_divergence_recur(sub_area, area)
        inter_div += local_pop_proportion * sub_area['Residential Divergence']
    between_div = calc_resident_between_divergence(area)
    value = inter_div + between_div
    if area['Valid'] and area['POP'] > 1000:
        Loading.residentdiv.append(value)
    return value


def calc_resident_between_divergence(area):
    div = 0
    sub = area['sub']
    for sub_area in sub:
        local_pop_proportion = sub_area['POP'] / area['POP']
        div += local_pop_proportion * calc_divergence_contribution(sub_area, area)
    return div


def calc_div_districts(districts):
    for district in districts:
        district['Divergence'] = calc_divergence(district)
    for district in districts:
        district['Residential Divergence'] = calc_resident_divergence(district)





def calc_resident_iso(area):
    iso = calc_resident_iso_recur(area, area)
    if area['POP'] == 0:
        return 0
    p = area['BROWN'] / area['POP']
    value = abs(iso - p)
    if not is_lowest_level(area) and area['Valid'] and area['POP'] > 2000:
        Loading.residentiso.append(value)

    return value


def calc_resident_iso_recur(area, super_area):
    if is_lowest_level(area):
        return calc_iso_contribution(area, super_area)
    iso_contribution = 0
    for sub_area in area['sub']:
        iso_contribution += calc_resident_iso_recur(sub_area, super_area)
    return iso_contribution


def calc_iso_districts(districts):
    for district in districts:
        district['Isolation'] = calc_iso(district)
    for district in districts:
        district['Residential Isolation'] = calc_resident_iso(districts)


def split(america):
    states = []
    counties = []
    tracts = []
    for state in america['sub']:
        for county in state['sub']:
            for tract in county['sub']:
                tracts.append(tract)
            county.pop('sub')
            counties.append(county)
        state.pop('sub')
        states.append(state)
    america.pop('sub')
    return america, states, counties, tracts


def find_state(states, fip):
    for state in states:
        if state['state'] == fip:
            return state


def find_county(counties, fip):
    for county in counties:
        if county['county'] == fip:
            return county


def calc_iso_contribution(sub_area, area):
    t1 = 0 if area['BROWN'] == 0 else sub_area['BROWN'] / area['BROWN']
    t2 = 0 if sub_area['POP'] == 0 else sub_area['BROWN'] / sub_area['POP']
    return t1 * t2


def calc_iso(area):
    iso = calc_iso_recur(area, area)
    if area['POP'] == 0:
        return 0
    p = area['BROWN'] / area['POP']
    value = abs(iso - p)
    if not is_lowest_level(area) and area['Valid'] and area['POP'] > 2000:
        Loading.iso_distribution.append(value)

    return value


def calc_iso_recur(area, super_area):
    if is_lowest_level(area):
        return calc_iso_contribution(area, super_area)
    iso_contribution = 0
    for sub_area in area['sub']:
        iso_contribution += calc_iso_recur(sub_area, super_area)
    return iso_contribution


def calc_divergence(area: dict):
    return calc_divergence_recur(area, None)


def calc_divergence_recur(area: dict, super_area):
    if is_lowest_level(area):
        return calc_divergence_contribution(area, super_area)
    inter_div = 0
    for sub_area in area['sub']:
        local_pop_proportion = sub_area['POP'] / area['POP']
        sub_area['Divergence'] = calc_divergence_recur(sub_area, area)
        inter_div += local_pop_proportion * sub_area['Divergence']
    between_div = calc_between_divergence(area)
    value = inter_div + between_div
    if area['Valid'] and area['POP'] > 2000:
        Loading.div_distribution.append(value)
    return value


def calc_between_divergence(area):
    div = 0
    sub = area['sub']
    for sub_area in sub:
        local_pop_proportion = sub_area['POP'] / area['POP']
        div += local_pop_proportion * calc_divergence_contribution(sub_area, area)
    return div


def calc_divergence_contribution(sub_area, area):
    pop = sub_area['POP']
    if area is None:
        return 0
    pop_tot = area['POP']
    if pop == 0:
        return 0

    brown_proportion = sub_area['BROWN'] / pop
    brown_proportion_tot = area['BROWN'] / pop_tot

    non_brown_proportion = get_non_brown(sub_area) / pop
    non_brown_proportion_tot = get_non_brown(area) / pop_tot

    brown_div = 0
    if brown_proportion != 0 and brown_proportion_tot != 0:
        brown_div = brown_proportion * log(brown_proportion / brown_proportion_tot, 2)
    non_brown_div = 0
    if non_brown_proportion != 0 and non_brown_proportion_tot != 0:
        non_brown_div = non_brown_proportion * log(non_brown_proportion / non_brown_proportion_tot, 2)

    return brown_div + non_brown_div


def get_non_brown(area):
    return area['POP'] - area['BROWN']


def is_lowest_level(area):
    return 'sub' not in area.keys()
