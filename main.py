import json
import os
from copy import deepcopy

from matplotlib import axes, pyplot as plt
from matplotlib.figure import Figure

# import Loading.Education_Formatting
import Loading.LoadEducational
import Loading.LoadResidental
import Loading.calc_indexes
import Loading.calc_statistics
import Loading.clean_data
import Loading.put_school_data
from Loading import export


def plot_distributions(level):
    fig: Figure
    ax: axes.Axes
    fig, ax = plt.subplots()

    combined = []
    if len(Loading.div_distribution) != len(Loading.iso_distribution):
        print('amongus')
    for i in range(len(Loading.div_distribution)):
        combined.append((Loading.div_distribution[i] + Loading.iso_distribution[i]) / 2)
    ax.set_title(f'Combined Index for all geography levels in the US based on {level}')
    ax.set_xlabel('Combined Index')
    ax.set_ylabel('Count')
    ax.hist(combined)

    # fig, ax = plt.subplots()
    # ax.set_title(f'Divergence Index for all geography levels in the US based on {level}')
    # ax.set_xlabel('Divergence Value')
    # ax.set_ylabel('Count')
    # ax.hist(Loading.div_distribution)

    plt.show()


# def blocks():
#     f = open('data/America_Blocks.json', 'r')
#     america = json.load(f)
#     Loading.calc_indexes.calc_div_us(america)
#     Loading.calc_indexes.calc_iso_us(america)
#     with open(f'data/America_Blocks_Indexed.json', 'w') as fp:
#         json.dump(america, fp)
#     plot_distributions('Blocks')
#     america, states, counties, tracts = Loading.calc_indexes.split(america)
#     Loading.calc_indexes.rank(states)
#
#     Loading.calc_indexes.rank(counties)
#
#     export(states, f'States_Blocks')
#     export(america, f'United States_Blocks')
#     export(counties, f'Counties_Blocks')
#     export(tracts, f'Tracts_Blocks')
#     print('___Blocks___')
#     print('__Counties__')
#     Loading.calc_statistics.calc_correlation(counties)
#     print('__States__')
#     Loading.calc_statistics.calc_correlation(states)


def schools():
    districts ={}
    f = open(f'data/Schools/Districts/California.json')
    districts['sub'] = json.load(f)
    Loading.calc_indexes.calc_div_districts(districts)
    Loading.calc_indexes.calc_iso_districts(districts)
    Loading.calc_indexes.rank(districts)
    Loading.calc_indexes.resident_rank(districts)

    plot_distributions('School Districts')
    Loading.calc_statistics.calc_correlation(districts)

    with open(f'data/Schools/Indexed_w_resident_Districts.json', 'w') as fp:
        json.dump(districts, fp)


def tracts():
    f = open('data/tracts/America.json', 'r')
    america: dict = json.load(f)
    Loading.calc_indexes.calc_div_us(america)
    Loading.calc_indexes.calc_iso_us(america)

    plot_distributions('Tracts')
    copy = deepcopy(america)
    us, states, counties, tracts = Loading.calc_indexes.split(copy)
    Loading.calc_indexes.rank(states)

    Loading.calc_indexes.rank(counties)
    Loading.calc_indexes.rerank_america(america, states, counties)

    with open(f'data/tracts/America_Indexed.json', 'w') as fp:
        json.dump(america, fp)
    export(states, f'tracts/States')
    export(us, f'tracts/US')
    export(counties, f'tracts/Counties')
    export(tracts, f'tracts/Tracts')
    print('**___Tracts___**')
    print('__Counties__')
    Loading.calc_statistics.calc_correlation(counties)
    print('__States__')
    Loading.calc_statistics.calc_correlation(states)


def main():
    # tracts()
    schools()
    # Loading.LoadResidental.load_racial_data()
    # Loading.LoadEducational.open_districts()
    # Loading.put_school_data.put_blocks_in_districts()
    # import requests
    #
    # url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=+31.4097368,-085.7458071destinations=New%20York%20City%2C%20NY&units=imperial&key=AIzaSyDNQ1aoiCafUo-ahEGqC4DeNtzWsp8FWEo"
    # x = {"Valid": True, "NAME": "FREMONT UNION HIGH", "STATE": "California", "Agency ID": "0614430",
    #  "COUNTY": "Santa Clara County", "county": "06085", "state": "06", "URL": "http://www.fuhsd.org", "BROWN": 1696,
    #  "POP": 11032, "sub": [
    #     {"Valid": True, "NAME": "COMMUNITY DAY", "School ID": "061443008353", "Agency ID": "0614430", "URL": '',
    #      "low": "9th Grade", "high": "12th Grade", "level": "High", "state": "06", "lat": "37.352767",
    #      "long": "-122.037507", "POP": 15, "BROWN": 10, "Divergence": 0.9629676558482418},
    #     {"Valid": True, "NAME": "CUPERTINO HIGH", "School ID": "061443001695", "Agency ID": "0614430", "URL": '',
    #      "low": "9th Grade", "high": "12th Grade", "level": "High", "state": "06", "lat": "37.320237",
    #      "long": "-122.009606", "POP": 2278, "BROWN": 230, "Divergence": 0.017211624274271378},
    #     {"Valid": True, "NAME": "FREMONT HIGH", "School ID": "061443001696", "Agency ID": "0614430", "URL": '',
    #      "low": "9th Grade", "high": "12th Grade", "level": "High", "state": "06", "lat": "37.352648",
    #      "long": "-122.034123", "POP": 2172, "BROWN": 915, "Divergence": 0.2953845942432055},
    #     {"Valid": True, "NAME": "HOMESTEAD HIGH", "School ID": "061443001697", "Agency ID": "0614430", "URL": '',
    #      "low": "9th Grade", "high": "12th Grade", "level": "High", "state": "06", "lat": "37.336243",
    #      "long": "-122.048487", "POP": 2430, "BROWN": 389, "Divergence": 0.00022094569558053605},
    #     {"Valid": True, "NAME": "LYNBROOK HIGH", "School ID": "061443001698", "Agency ID": "0614430", "URL": '',
    #      "low": "9th Grade", "high": "12th Grade", "level": "High", "state": "06", "lat": "37.300837",
    #      "long": "-122.003803", "POP": 1944, "BROWN": 68, "Divergence": 0.10811139985603214},
    #     {"Valid": True, "NAME": "MONTA VISTA HIGH", "School ID": "061443001699", "Agency ID": "0614430", "URL": '',
    #      "low": "9th Grade", "high": "12th Grade", "level": "High", "state": "06", "lat": "37.314500",
    #      "long": "-122.056192", "POP": 2193, "BROWN": 84, "Divergence": 0.10061069760746617}]}
    # print(Loading.calc_indexes.calc_divergence(x))
    # print(Loading.calc_indexes.calc_iso(x))
    # schools = []
    # for school in x['sub']:
    #     schools.append([int(school['BROWN']), int(school['POP'])])
    # print(Loading.calc_indexes.calc_list_seg(schools))
    # payload = {}
    # headers = {}
    #
    # response = requests.request("GET", url, headers=headers, data=payload)
    #
    # print(response.text)
    # import geopandas as gpd
    # amongus = gpd.read_file('data/geojson/geo_districts/06.json')
    # if 'Schools' in amongus:
    #     print('i am homosexual')
    # Loading.LoadEducational.add_data_to_geo()
    # Loading.put_school_data.put_blocks_in_districts()
    # Loading.put_school_data.IHATEGOOGLE()
    # print('hi')
    # response = requests.get('https://api.census.gov/data/2020/dec/pl?get=NAME&for=school%20district%20(elementary)%20(or%20part):99999&in=state:72%20congressional%20district:98')
    # print(c.pl.get("NAME", geo={'for': 'county:*',
    #                               'in': 'state:01'}))

    # read_csv function which is used to read the required CSV file
    # list = ['GISJOIN','YEAR','GEOID','GEOCODE','REGIONA','DIVISIONA','STATE','STATEA','COUNTY','COUNTYA','COUSUBA','COUSUBCC','SUBMCDA','CONCITA','PLACEA','PLACECC','TRACTA','BLKGRPA','BLOCKA','AIANHHA','RES_ONLYA','TRUSTA','AIANHHCC','AITSA','ANRCA','CBSAA','MEMI','CSAA','METDIVA','NECTAA','NMEMI','CNECTAA','NECTADIVA','CBSAPCI','NECTAPCI','CDA','SLDU18A','SLDL18A','VTDA','VTDI','SDELMA','SDSECA','SDUNIA','AREALAND','AREAWATR','BASENAME','NAME','FUNCSTAT','INTPTLAT','INTPTLON','LSADC','U7B001','U7B002','U7B003','U7B004','U7B005','U7B006','U7B007','U7B008','U7B009','U7B010','U7B011','U7B012','U7B013','U7B014','U7B015','U7B016','U7B017','U7B018','U7B019','U7B020','U7B021','U7B022','U7B023','U7B024','U7B025','U7B026','U7B027','U7B028','U7B029','U7B030','U7B031','U7B032','U7B033','U7B034','U7B035','U7B036','U7B037','U7B038','U7B039','U7B040','U7B041','U7B042','U7B043','U7B044','U7B045','U7B046','U7B047','U7B048','U7B049','U7B050','U7B051','U7B052','U7B053','U7B054','U7B055','U7B056','U7B057','U7B058','U7B059','U7B060','U7B061','U7B062','U7B063','U7B064','U7B065','U7B066','U7B067','U7B068','U7B069','U7B070','U7B071']
    #
    # for i, val in enumerate(list):
    #     print(i, val)

    # data = pd.read_csv('data/raw_blocks/I hate this.csv', on_bad_lines='skip',encoding='utf8')
    # Loading.put_school_data.split_into_states()
    # Loading.put_school_data.add_school_ids()
    # print(c.pl.get(('NAME','SDUNIA'),
    #                 geo={'for': 'block:*',
    #                      'in': f'state:01 county:001 tract:020100'}))


if __name__ == "__main__":
    main()
