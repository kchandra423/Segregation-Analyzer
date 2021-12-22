import Loading.Load_Data
import Loading.calc_metrics
import Loading.Education_Formatting
import Loading.calc_statistics
from Reading import Read_Data


def main():
    # Loading.Load_Data.load_racial_data()
    # Loading.Update_DB.calculate_us()
    # Loading.Education_Formatting.clean_education_data()
    # Loading.calc_metrics.calculate_districts()
    Loading.calc_statistics.compile_district_stats()

if __name__ == "__main__":
    main()
