from Loading import counties, blocks_groups, states, united_states


def calculate_us():
    america = united_states.find_one()
    america_dis = 0
    america_iso = 0
    contributions = []
    brown = america['BROWN']
    non_brown = america["POP"] - brown
    for state in america['States'].values():
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
    counties_in_state = state['Counties']
    contributions = []
    brown = state['BROWN']
    non_brown = state['POP'] - brown
    for county in counties_in_state.values():
        county = counties.find_one({'_id': county})
        results = calculate_county(county, state_info=(brown, non_brown), us_info=us_info)

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
    for block_group in county['Blocks']:
        block = blocks_groups.find_one(block_group)
        brown = block['BROWN']
        non_brown = block['POP'] - brown
        dis_contribution_county = calc_dis_contribution(brown, brown_county, non_brown, non_brown_county)
        iso_contribution_county = calc_iso_contribution(brown, brown_county, non_brown)
        state_dis_contribution += calc_dis_contribution(brown, state_info[0], non_brown, state_info[1])
        state_iso_contribution += calc_iso_contribution(brown, state_info[0], non_brown)
        us_dis_contribution += calc_dis_contribution(brown, us_info[0], non_brown, us_info[1])
        us_iso_contribution += calc_iso_contribution(brown, us_info[0], non_brown)
        contributions.append([block['_id'], dis_contribution_county, iso_contribution_county])
        county_dis += dis_contribution_county
        county_iso += iso_contribution_county
    for i in range(len(contributions)):
        contributions[i][1] /= county_dis if county_dis > 0 else 1
        contributions[i][2] /= county_iso if county_iso > 0 else 1
    update_contributions(contributions, blocks_groups)
    update_indexes(county['_id'], county_dis, county_iso, counties)

    print(f'Finished {county["NAME"]}')
    return state_dis_contribution, state_iso_contribution, us_dis_contribution, us_iso_contribution


def update_contributions(areas, collection):
    for area in areas:
        collection.update_one({'_id': area[0]}, {'$set':
            {
                'Dissimilarity Contribution': area[1],
                'Isolation Contribution': area[2]
            }})


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
