import json

import Loading.Education_Formatting
import Loading.Load_Data
import Loading.calc_indexes
import Loading.calc_statistics


def main():
    # f = open('data/America.json', 'r')
    # america = json.load(f)
    # Loading.calc_indexes.calc_iso_us(america)
    # Loading.calc_indexes.calc_div_us(america)
    # with open(f'data/America_Indexed.json', 'w') as fp:
    #     json.dump(america, fp)

    # f = open('data/America_Indexed.json', 'r')
    # america = json.load(f)
    # Loading.calc_indexes.split(america)

    Loading.Load_Data.load_racial_data()
    # Loading.calc_indexes.calc_iso_us()
    # Loading.Update_DB.calculate_us()
    # Loading.Education_Formatting.clean_education_data()
    # Loading.calc_metrics.calculate_districts()

    # Loading.calc_statistics.calc_correlation('Counties')
    # Loading.calc_statistics.calc_correlation('States')
    # Reading.Read_Data.get_info(input('Enter a state'))


if __name__ == "__main__":
    main()
