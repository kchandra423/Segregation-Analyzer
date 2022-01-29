import json


def is_valid(area):
    return area['POP'] > 0 and area['BROWN'] > 0 and (area['BROWN'] / area['POP']) >= 0.01


def clean():
    f = open('data/America_Blocks.json', 'r')
    america = json.load(f)
    america['Valid'] = is_valid(america)
    for state in america['Sub_Areas']:
        state['Valid'] = is_valid(state)
        for county in state['Sub_Areas']:
            county['Valid'] = is_valid(county)
            for tract in county['Sub_Areas']:
                tract['Valid'] = is_valid(tract)
                for block in tract['Sub_Areas']:
                    block['Valid'] = is_valid(block)
    with open(f'data/America_Blocks.json', 'w') as fp:
        json.dump(america, fp)
