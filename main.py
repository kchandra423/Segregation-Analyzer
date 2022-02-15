import json
from copy import deepcopy

from matplotlib import axes, pyplot as plt
from matplotlib.figure import Figure

import Loading.calc_indexes
import Loading.calc_statistics
import Loading.clean_data
from Loading.Load_Data import export


def plot_distributions(level):
    fig: Figure
    ax: axes.Axes
    fig, ax = plt.subplots()
    ax.set_title(f'Isolation Index for all geography levels in the US based on {level}')
    ax.set_xlabel('Isolation Value')
    ax.set_ylabel('Count')
    ax.hist(Loading.iso_distribution)

    fig, ax = plt.subplots()
    ax.set_title(f'Divergence Index for all geography levels in the US based on {level}')
    ax.set_xlabel('Divergence Value')
    ax.set_ylabel('Count')
    ax.hist(Loading.div_distribution)

    plt.show()


def blocks():
    f = open('data/America_Blocks.json', 'r')
    america = json.load(f)
    Loading.calc_indexes.calc_div_us(america)
    Loading.calc_indexes.calc_iso_us(america)
    with open(f'data/America_Blocks_Indexed.json', 'w') as fp:
        json.dump(america, fp)
    plot_distributions('Blocks')
    america, states, counties, tracts = Loading.calc_indexes.split(america)
    Loading.calc_indexes.rank(states)

    Loading.calc_indexes.rank(counties)

    export(states, f'States_Blocks')
    export(america, f'United States_Blocks')
    export(counties, f'Counties_Blocks')
    export(tracts, f'Tracts_Blocks')
    print('___Blocks___')
    print('__Counties__')
    Loading.calc_statistics.calc_correlation(counties)
    print('__States__')
    Loading.calc_statistics.calc_correlation(states)


def schools():
    f = open('data/Schools/Districts.json')
    districts = json.load(f)

    Loading.calc_indexes.calc_div_districts(districts)
    Loading.calc_indexes.calc_iso_districts(districts)
    with open(f'data/Schools/Indexed_Districts.json', 'w') as fp:
        json.dump(districts, fp)


def tracts():
    f = open('data/Tracts/America_Tracts.json', 'r')
    america: dict = json.load(f)
    Loading.calc_indexes.calc_div_us(america)
    Loading.calc_indexes.calc_iso_us(america)
    plot_distributions('Tracts')
    copy = deepcopy(america)
    us, states, counties, tracts = Loading.calc_indexes.split(copy)
    Loading.calc_indexes.rank(states)

    Loading.calc_indexes.rank(counties)
    Loading.calc_indexes.rerank_america(america, states, counties)

    with open(f'data/Tracts/America_Tracts_Indexed.json', 'w') as fp:
        json.dump(america, fp)
    export(states, f'Tracts/States_Tracts')
    export(us, f'Tracts/United States_Tracts')
    export(counties, f'Tracts/Counties_Tracts')
    export(tracts, f'Tracts/Tracts_Tracts')
    print('**___Tracts___**')
    print('__Counties__')
    Loading.calc_statistics.calc_correlation(counties)
    print('__States__')
    Loading.calc_statistics.calc_correlation(states)


def main():
    # blocks()
    # tracts()
    # Loading.Load_Data.open_districts()
    schools()

if __name__ == "__main__":
    main()
