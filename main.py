import Loading.Load_Data
import Loading.calc_metrics
import Loading.Education_Formatting
import Loading.calc_statistics
import Loading.calc_indexes
import Reading.Read_Data
from Reading import Read_Data


def main():
    # Loading.Load_Data.load_racial_data()
    Loading.calc_indexes.calc_us()
    # Loading.Update_DB.calculate_us()
    # Loading.Education_Formatting.clean_education_data()
    # Loading.calc_metrics.calculate_districts()
    # Loading.calc_statistics.compile_district_stats()
    # Reading.Read_Data.get_info(input('Enter a state'))

if __name__ == "__main__":
    main()
