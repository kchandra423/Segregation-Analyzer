import statistics
from matplotlib import pyplot as plt
import numpy as np
from Loading import client


def compile_district_stats():
    districts = client.get_database("EducationData").get_collection('Districts').find()
    dis_districts = []
    iso_districts = []
    for district in districts:
        dis_districts.append(district["Dissimilarity"])
        iso_districts.append(district['Isolation'])
    dis_vals = np.array(dis_districts)
    iso_vals = np.array(iso_districts)
    fig, ax = plt.subplots(1, 1)
    ax.hist(dis_vals)
    plt.show()

    fig, ax = plt.subplots(1, 1)
    ax.hist(iso_vals)
    plt.show()
    print(sorted(dis_districts)[100:105])

    print(sorted(dis_districts)[-105:-100])
    print(statistics.mean(dis_districts))
    print(statistics.stdev(dis_districts))
    print(statistics.mean(iso_districts))
    print(statistics.stdev(iso_districts))
    print(statistics.correlation(dis_districts, iso_districts))
