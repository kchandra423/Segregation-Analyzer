import pymongo

from Loading import client

db = client.get_database('ResidentialData')
counties = db.get_collection("Counties")

tracts = db.get_collection('Tracts')

states = db.get_collection('States')

blocks_groups = db.get_collection('Blocks')

united_states = db.get_collection('United States')


def calculate_us():
    america = united_states.find_one()
    america_dis = 0
    america_iso = 0
    contributions = []
    brown = america['BROWN']
    non_brown = america["POP"] - brown
    _states = states.find()
    for state in _states:
        results = calculate_state(state, us_info=(brown, non_brown))
        contributions.append([state['_id'], results[0], results[1]])

        america_dis += results[0]
        america_iso += results[1]
    for i in range(len(contributions)):
        contributions[i][1] /= america_dis if america_dis > 0 else 1
        contributions[i][2] /= america_iso if america_iso > 0 else 1

    update_contributions(contributions, states)
    update_indexes(america['_id'], america_dis, america_iso, united_states)


def calculate_state(state: dict, us_info):
    state_dis = 0
    state_iso = 0
    us_dis_contribution = 0
    us_iso_contribution = 0
    ids = state['Counties']
    contributions = []
    brown = state['BROWN']
    non_brown = state['POP'] - brown
    all_counties = counties.find({'state': state['state']})
    all_blocks = list(blocks_groups.find({'state': state['state']}))
    all_tracts = list(tracts.find({'state': state['state']}))
    for county in all_counties:
        results = calculate_county(county, (brown, non_brown), us_info, find_in_county(all_tracts, county),
                                   find_in_county(all_blocks, county))

        contributions.append([county['_id'], results[0], results[1]])
        us_dis_contribution += results[2]
        us_iso_contribution += results[3]
        state_dis += results[0]
        state_iso += results[1]

    for i in range(len(contributions)):
        contributions[i][1] /= state_dis if state_dis > 0 else 1
        contributions[i][2] /= state_iso if state_iso > 0 else 1
    update_contributions(contributions, counties)
    update_indexes(state['_id'], state_dis, state_iso, states)
    print(f'Finished {state["NAME"]}')
    return us_dis_contribution, us_iso_contribution


# state_pop = state_nonbrown
def calculate_county(county: dict, state_info, us_info, tracts_in_county, blocks_in_county):
    state_dis_contribution = 0
    state_iso_contribution = 0
    us_dis_contribution = 0
    us_iso_contribution = 0
    brown_county = county['BROWN']
    non_brown_county = county['POP'] - brown_county
    contributions = []
    county_dis = 0
    county_iso = 0
    for tract in tracts_in_county:
        results = calculate_tract((brown_county, non_brown_county), state_info, us_info,
                                  find_in_tract(blocks_in_county, tract))
        contributions.append([tract['_id'], results[0], results[1]])

        county_dis += results[0]
        county_iso += results[1]
        state_dis_contribution += results[2]
        state_iso_contribution += results[3]
        us_dis_contribution += results[4]
        us_iso_contribution += results[5]

    for i in range(len(contributions)):
        contributions[i][1] /= county_dis if county_dis > 0 else 1
        contributions[i][2] /= county_iso if county_iso > 0 else 1
    # print(contributions)
    update_contributions(contributions, tracts)
    update_indexes(county['_id'], county_dis, county_iso, counties)

    print(f'Finished {county["NAME"]}')
    return state_dis_contribution, state_iso_contribution, us_dis_contribution, us_iso_contribution


def calculate_tract(county_info, state_info, us_info, blocks_in_tract):
    state_dis_contribution = 0
    state_iso_contribution = 0
    us_dis_contribution = 0
    us_iso_contribution = 0
    county_dis_contribution = 0
    county_iso_contribution = 0
    brown_county = county_info[0]
    non_brown_county = county_info[1]
    for block in blocks_in_tract:
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


def find_in_tract(areas: list, tract):
    result = []
    for area in areas:
        if area['tract'] == tract['tract'] and area['county'] == tract['county'] and area['state'] == tract['state']:
            result.append(area)
    return result


def find_in_county(areas: list, county):
    result = []
    for area in areas:
        if area['county'] == county['county'] and area['state'] == county['state']:
            result.append(area)
    return result


def find_in_state(areas: list, state):
    result = []
    for area in areas:
        if area['state'] == area['state']:
            result.append(area)
    return result


def update_contributions(areas, collection):
    updates = []
    for area in areas:
        updates.append(pymongo.UpdateOne({'_id': area[0]}, {'$set':
            {
                'Dissimilarity Contribution': area[1],
                'Isolation Contribution': area[2]
            }}))
    collection.bulk_write(updates)


def update_indexes(_id, dis, iso, collection):
    collection.update_one({'_id': _id}, {'$set': {
        'Dissimilarity': dis,
        'Isolation': iso
    }})


def calc_dis_contribution(brown, brown_tot, non_brown, non_brown_tot):
    return 0.5 * abs(brown / (brown_tot if brown_tot > 0 else 1) - non_brown / (
        non_brown_tot if non_brown_tot > 0 else 1))


def calc_iso_contribution(brown, brown_tot, non_brown):
    pop = brown + non_brown
    return (brown / (brown_tot if brown_tot > 0 else 1)) * (
            brown / (pop if pop > 0 else 1))
