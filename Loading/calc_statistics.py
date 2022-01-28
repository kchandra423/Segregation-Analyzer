import json

import numpy as np
from matplotlib import pyplot as plt


def calc_correlation(level):
    f = open(f'data/{level}.json', 'r')
    areas = json.load(f)
    divs = []
    isos = []
    names = []
    proportion = []
    for area in areas:
        if 'Invalid' not in area.keys():
            divs.append(area['Divergence'])
            isos.append(area['Isolation'])
            proportion.append(area['BROWN'] / area['POP'])
            names.append(area['NAME'])
    fig, ax = plt.subplots()
    ax.set_xlabel('Isolation')
    ax.set_ylabel('Divergence')
    ax.scatter(isos, divs)
    # for i in range(len(names)):
    #     ax.annotate(names[i], (isos[i], divs[i]))

    fig, (ax2, ax3) = plt.subplots(2)

    ax2.set_xlabel('Brown proportion')
    ax2.set_ylabel('Divs')
    ax2.scatter(proportion, divs)

    ax3.set_xlabel('Brown proportion')
    ax3.set_ylabel('Isolation')
    ax3.scatter(proportion, isos)
    plt.show()
    print(np.corrcoef(np.array(isos), np.array(divs))[0][1])

    print(np.corrcoef(np.array(proportion), np.array(divs))[0][1])

    print(np.corrcoef(np.array(proportion), np.array(isos))[0][1])
