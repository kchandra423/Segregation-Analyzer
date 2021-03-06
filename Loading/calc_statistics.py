import json

import numpy as np
from matplotlib import pyplot as plt


def calc_correlation(areas):
    divs = []
    isos = []
    names = []
    proportion = []
    for area in areas:
        if area['Valid']:
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

    ax2.set_xlabel('Proportion of Brown Population')
    ax2.set_ylabel('Divergence Index')
    ax2.scatter(proportion, divs)

    ax3.set_xlabel('Proportion of Brown Population')
    ax3.set_ylabel('Isolation Index')
    ax3.scatter(proportion, isos)
    plt.subplots_adjust(left=0.1,
                        bottom=0.1,
                        right=0.9,
                        top=0.9,
                        wspace=0.4,
                        hspace=0.4)
    plt.show()
    print(f'Iso to div :{np.corrcoef(np.array(isos), np.array(divs))[0][1]}')

    print(f'Proportion to div: {np.corrcoef(np.array(proportion), np.array(divs))[0][1]}')

    print(f'Proportion to iso: {np.corrcoef(np.array(proportion), np.array(isos))[0][1]}')
