import json


def remove_blocks():
    f = open('data/America.json', 'r')
    america = json.load(f)
    for state in america['States']:
        for county in state['Counties']:
            for tract in county['Tracts']:
                tract.pop('Blocks')
            print(f'Finished {county["NAME"]}')
    with open(f'data/America_No_Blocks.json', 'w') as fp:
        json.dump(america, fp)
