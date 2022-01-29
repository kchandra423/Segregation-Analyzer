import json

from matplotlib import pyplot as plt, axes
from matplotlib.figure import Figure

import Loading.calc_indexes
import Loading.clean_data


def main():
    # f = open('data/America_Blocks.json', 'r')
    # america = json.load(f)
    # Loading.calc_indexes.calc_iso_us(america)
    # Loading.calc_indexes.calc_div_us(america)
    # with open(f'data/America_Indexed.json', 'w') as fp:
    #     json.dump(america, fp)
    # print(Loading.number)
    # fig: Figure
    # ax: axes.Axes
    # fig, ax = plt.subplots()
    # ax.set_title('Modified Isolation Index for all geography levels in the US')
    # ax.set_xlabel('Isolation Value')
    # ax.set_ylabel('Count')
    # ax.hist(Loading.distribution)
    # plt.show()

    # Loading.clean_data.clean()
    f = open('data/America_Indexed.json', 'r')
    america = json.load(f)
    # america['Sub_Areas'] = america.pop('States')
    # for state in america['Sub_Areas']:
    #     state['Sub_Areas'] = state.pop('Counties')
    #     for county in state['Sub_Areas']:
    #         county['Sub_Areas'] = county.pop('Tracts')
    #         for tract in county['Sub_Areas']:
    #             tract['Sub_Areas'] = tract.pop('Blocks')
    # with open(f'data/America_Blocks.json', 'w') as fp:
    #     json.dump(america, fp)

    Loading.calc_indexes.split(america)
    # Loading.Load_Data.load_racial_data()
    # Loading.calc_indexes.calc_iso_us()
    # Loading.Update_DB.calculate_us()
    # Loading.Education_Formatting.clean_education_data()
    # Loading.calc_metrics.calculate_districts()

    # Loading.calc_statistics.calc_correlation('Counties')
    # Loading.calc_statistics.calc_correlation('States')
    # Reading.Read_Data.get_info(input('Enter a state'))


if __name__ == "__main__":
    main()
