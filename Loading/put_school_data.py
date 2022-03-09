import csv
import json
import os
import pprint

import geojson
import us

blocks_without = 0


def find_block(blocks, state, county, tract, block_fip):
    # try:
    #     x = blocks[state][county][tract]
    # except:
    #     return None
    for block in blocks[state][county][tract]:
        if block['block'] == block_fip:
            return block
    print('couldnt find one')


def index_json(blocks):
    index = {}
    for block in blocks:
        if block['state'] not in index.keys():
            index[block['state']] = {}
        state = index[block['state']]
        if block['county'] not in state.keys():
            state[block['county']] = {}
        county = state[block['county']]
        if block['tract'] not in county.keys():
            county[block['tract']] = []
        tract = county[block['tract']]
        tract.append(block)
    return index


def addinfo(geo, json):
    json = index_json(json)
    for place in geo['features']:
        place = place['properties']

        del place["GEOID20"]
        del place["UACE20"]
        del place["UATYPE20"]
        del place["ALAND20"]
        del place["AWATER20"]
        del place["FUNCSTAT20"]
        del place['UR20']
        del place["MTFCC20"]
        del place["HOUSING20"]
        del place["POP20"]
        place['NAME'] = place.pop("NAME20")
        place['lat'] = place.pop("INTPTLAT20")
        place['long'] = place.pop("INTPTLON20")
        place['state'] = place.pop('STATEFP20')
        place['county'] = place.pop('COUNTYFP20')
        place['tract'] = place.pop('TRACTCE20')
        place['block']= place.pop('BLOCKCE20')

        place['GEOID'] = place['state'] + place['county'] + place['tract'] + place['block']
        info = find_block(json, place['state'], place['county'], place['tract'], place['block'])
        if info is None:
            print('couldnt find one')
            place['BROWN'] = None
            place['POP'] = None
            place['elementary'] = None
            place['secondary'] = None
            place['unified'] = None
            continue
        place['BROWN'] = info['BROWN']
        place['POP'] = info['POP']
        place['elementary'] = info['elementary']
        place['secondary'] = info['secondary']
        place['unified'] = info['unified']


def IHATEGOOGLE():
    import os
    import us
    import json
    for geo in os.listdir("data/geojson/oldblocks"):
        if 'ds_store' in geo.lower():
            continue
        fip = geo[8:10]
        print(fip)
        if int(fip) > 56:
            continue
        f = open(f'data/Schools/blocks_with_schools/{str(us.states.lookup(fip))}.json', 'r')
        info = json.load(f)

        f = open(f'data/geojson/oldblocks/{geo}', 'r')
        geo_json = geojson.load(f)
        addinfo(geo_json, info)
        with open(f'data/geojson/newBlocks/{geo[8:10]}.json', 'w') as fp:
            geojson.dump(geo_json, fp)
        print(geo)
        del geo_json
        del info


def split_into_states():
    with open('data/raw_blocks/Blocks.csv') as school_f:
        raw_blocks = csv.DictReader(school_f)
        curstate = ''
        curjson = []
        for raw_block in raw_blocks:
            if raw_block['STATE'] != curstate:
                if curjson is not None:
                    with open(f'data/Schools/raw_blocks_with_schools/{curstate}.json', 'w') as fp:
                        json.dump(curjson, fp)
                    print(f'Finished {curstate}')
                curjson = []
                curstate = raw_block["STATE"]
            curjson.append(raw_block)
        with open(f'data/Schools/raw_blocks_with_schools/{curstate}.json', 'w') as fp:
            json.dump(curjson, fp)


def index_json_raw(blocks):
    index = {}
    for block in blocks:
        if block['STATEA'] not in index.keys():
            index[block['STATEA']] = {}
        state = index[block['STATEA']]
        if block['COUNTYA'] not in state.keys():
            state[block['COUNTYA']] = {}
        county = state[block['COUNTYA']]
        if block['TRACTA'] not in county.keys():
            county[block['TRACTA']] = []
        tract = county[block['TRACTA']]
        tract.append(block)
    return index


def add_school_ids():
    for state in os.listdir('data/Schools/raw_blocks_with_schools'):
        print(state)

        if 'ds_store' in state.lower():
            continue
        f = open(f'data/Schools/raw_blocks_with_schools/{state}', 'r')
        school_json = json.load(f)
        f = open(f'data/Schools/Blocks/{state}')
        info_json = json.load(f)
        school_json = index_json_raw(school_json)
        for block in info_json:
            school_block = find_block(school_json, block['state'], block['county'], block['tract'], block['block'])
            block['elementary'] = school_block['SDELMA']
            block['secondary'] = school_block['SDSECA']
            block['unified'] = school_block['SDUNIA']
        with open(f'data/Schools/blocks_with_schools/{state}', 'w') as fp:
            json.dump(info_json, fp)

    # with open('data/raw_blocks/Blocks.csv') as school_f:
    #     raw_blocks = csv.DictReader(school_f)
    #     curstate = ''
    #     curjson = None
    #     n = 0
    #     try:
    #         for block in raw_blocks:
    #             if block['STATE'] != curstate:
    #                 if curjson is not None:
    #                     with open(f'data/Schools/blocks_with_schools/{curstate}.json', 'w') as fp:
    #                         json.dump(curjson, fp)
    #                     print(f'Finished {curstate}')
    #                 curstate = block["STATE"]
    #                 f = open(f'data/Schools/Blocks/{curstate}.json')
    #                 curjson = json.load(f)
    #             block_found = False
    #             for better_block in curjson:
    #                 if block['STATEA'] == better_block['state'] and block['COUNTYA'] == better_block['county'] and \
    #                         block[
    #                             'TRACTA'] == better_block['tract'] and block['BLOCKA'] == better_block['block']:
    #                     block_found = True
    #                     better_block['elementary'] = block['SDELMA']
    #                     better_block['secondary'] = block['SDSECA']
    #                     better_block['unified'] = block['SDUNIA']
    #                     break
    #             if not block_found:
    #                 print(
    #                     f'Couldnt find block for this block: {block["STATEA"]}, {block["COUNTYA"]}, {block["TRACTA"]}, {block["BLOCKA"]}')
    #         with open(f'data/Schools/blocks_with_schools/{curstate}.json', 'w') as fp:
    #             json.dump(curjson, fp)
    #     except Exception as e:
    #         print(n)


def find_district(districts, block: dict):
    districts = districts[block['state']]
    valids = [block.get('state') + block.get('secondary', '!'),
              block.get('state') + block.get('elementary', '!'),
              block.get('state') + block.get('unified', '!')]
    if '!' in valids[0] and '!' in valids[1] and '!' in valids[2]:
        global blocks_without
        blocks_without += 1
        return
    found = False
    for district in districts:
        if district['Agency ID'] in valids:
            district['Blocks'].append(block)
            found = True
    if not found and (block['secondary'] != '99999' and block['elementary'] != '99999' and block['unified'] != '99997'):
        print('uh oh')
        pprint.pprint(block)


def optimize_districts(districts):
    optimized = {}
    for district in districts:
        if district['state'] not in optimized.keys():
            optimized[district['state']] = []
        optimized[district['state']].append(district)
    return optimized


def put_blocks_in_districts():
    f = open('data/Schools/Indexed_Districts.json', 'r')
    districts = json.load(f)
    for district in districts:
        district['Blocks'] = []
    districts = optimize_districts(districts)
    for file in os.listdir('data/Schools/blocks_with_schools'):
        if 'ds_store' in file.lower():
            continue
        f = open(f'data/Schools/blocks_with_schools/{file}')
        blocks = json.load(f)
        for block in blocks:
            find_district(districts, block)
        print(f'Finished {file}')
    print(blocks_without)
    for state in districts:
        with open(f'data/Schools/Districts/{str(us.states.lookup(state))}.json', 'w') as fp:
            json.dump(districts[state], fp)
