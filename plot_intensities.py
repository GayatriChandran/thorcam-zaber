#!/usr/bin/env python
"""
Plot the power vs angle graph from a measurement (.csv file).

Gayatri 6/24
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

if __name__ == "__main__":

    file_name = 'air-07-21-2025-hwp-2-intensities.csv'                                   # Input file name

    df = pd.read_csv(file_name)

    ax = df.plot(x="Stage", y="Intensity", alpha=0.5, style='.-')
    ax.set_xlabel("Stage position (mm)")
    ax.set_ylabel("Sum of pixel values (a.u.)")
    # ax.set_xlim([2.3, 7.55])
    # ax.set_ylim([0, 30])
    ax.set_title(file_name)                                         # Plot

    plt.show()

    # fig = ax.get_figure()                                           # Save the picture
    # fig_name = file_name.rsplit('.csv')[0]
    # fig.savefig(fig_name)
