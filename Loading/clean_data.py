from Loading.calc_indexes import is_lowest_level


def is_valid(area):
    return area['POP'] > 0 and area['BROWN'] > 0 and (area['BROWN'] / area['POP']) >= 0.01


def clean(area):
    area['Valid'] = is_valid(area)
    if is_lowest_level(area):
        return
    for sub_area in area['Sub_Areas']:
        clean(sub_area)


def remove_PR(america):
    for state in america['Sub_Areas']:
        if state['NAME'] == "Puerto Rico":
            america['Sub_Areas'].remove(state)
