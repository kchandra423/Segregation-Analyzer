import json

from matplotlib import axes, pyplot as plt
from matplotlib.figure import Figure

import Loading.calc_indexes
import Loading.calc_statistics
import Loading.clean_data


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

    fig, ax = plt.subplots()
    ax.set_title(f'Chi2 for all geography levels in the US based on {level}')
    ax.set_xlabel('Chi2 probability')
    ax.set_ylabel('Count')
    ax.hist(Loading.chi_distribution)

    plt.show()


def blocks():
    f = open('data/America_Blocks.json', 'r')
    america = json.load(f)
    Loading.calc_indexes.calc_div_us(america)
    Loading.calc_indexes.calc_iso_us(america)
    Loading.calc_indexes.calc_chi_us(america)
    with open(f'data/America_Blocks_Indexed.json', 'w') as fp:
        json.dump(america, fp)
    plot_distributions('Blocks')
    america, states, counties, tracts = Loading.calc_indexes.split(america, 'Blocks')
    print('___Blocks___')
    print('__Counties__')
    Loading.calc_statistics.calc_correlation(counties)
    print('__States__')
    Loading.calc_statistics.calc_correlation(states)


def tracts():
    f = open('data/America_Tracts.json', 'r')
    america = json.load(f)
    Loading.calc_indexes.calc_div_us(america)
    Loading.calc_indexes.calc_iso_us(america)
    Loading.calc_indexes.calc_chi_us(america)
    with open(f'data/America_Tracts_Indexed.json', 'w') as fp:
        json.dump(america, fp)
    plot_distributions('Tracts')
    america, states, counties, tracts = Loading.calc_indexes.split(america, 'Tracts')
    print('___Tracts___')
    print('__Counties__')
    Loading.calc_statistics.calc_correlation(counties)
    print('__States__')
    Loading.calc_statistics.calc_correlation(states)


def main():
    # blocks()
    tracts()


if __name__ == "__main__":
    main()
