# Plotting tools

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
# Use non-interactive backend for plotting.
mpl.use('Agg')
# Enable use of LaTeX labels in plots.
plt.rcParams.update({"text.usetex": True, "text.latex.preamble": r"\usepackage{amsmath}"})
##########################################################################
# Scatter plot of periodicity candidates in the radio frequency vs. period diagram
def scatterplot_period_radiofreq(cand_periods, cand_freqs, cand_snrs, cand_flags, basename, min_period, max_period, min_freq, max_freq, plot_formats=['.png']):
    """
    Produce a scatter plot of periodicity detections in the radio frequency vs. trial period diagram.
    Candidate S/N values are shown on a color scale.
    Fundamental frequencies are displayed with a circular marker, whereas harmonics are indicated by a plus symbol.

    Parameters
    ----------
    cand_periods: 1D Numpy array
        Trial periods (s) of detected signals

    cand_freqs: 1D Numpy array
        Radio frequencies (MHz) corresponding to candidate detections

    cand_snrs: 1D Numpy array
        Matched filtering S/N values of detected candidates

    cand_flags: 1D Numpy array
        Harmonic flags ('F', 'S', or 'H') assigned to each candidate

    basename: string
        Output plot basename, including output path

    min_period: float
        Minimum trial period (s) shown on x-axis of plot

    max_period: float
        Maximum trial period (s) on x-axiss of plot

    min_freq: float
        Minimum radio frequency (MHz) limit on y-axis of plot

    max_freq: float
        Maximum radio frequency (MHz) shown on y-axis of plot

    plot_formats: list
        List of file formats for saving plot to disk
    """
    # Set up color map.
    cmap = plt.cm.cividis
    norm = mpl.colors.Normalize(vmin = np.min(cand_snrs), vmax = np.max(cand_snrs))
    # Begin plotting.
    fig1 = plt.figure(1, figsize=(7,6))
    marker_count = 0 # Keep track of the number of distinct marker shapes to plot.
    # Plot fundamental frequencies.
    f_idx = np.where(cand_flags=='F')[0]
    if len(f_idx) > 0:
        plt.scatter(x=cand_periods[f_idx], y=cand_freqs[f_idx], c=cand_snrs[f_idx], s=38, marker='o', cmap=cmap, norm=norm, label='Fundamental')
        marker_count += 1
    # Plot sub-harmonics.
    subharm_idx = np.where(cand_flags=='S')[0]
    if len(subharm_idx) > 0:
        plt.scatter(x=cand_periods[subharm_idx], y=cand_freqs[subharm_idx], c=cand_snrs[subharm_idx], s=38, marker='+', cmap=cmap, norm=norm, label='Subharmonic')
        marker_count += 1
    # Plot harmonics.
    harm_idx = np.where(cand_flags=='H')[0]
    if len(harm_idx) > 0:
        plt.scatter(x=cand_periods[harm_idx], y=cand_freqs[harm_idx], c=cand_snrs[harm_idx], s=38, marker='x', cmap=cmap, norm=norm, label='Harmonic')
        marker_count += 1
    # Set up colorbar.
    cbar = plt.colorbar(plt.cm.ScalarMappable(cmap = cmap, norm = norm))
    cbar.set_label('Matched filtering S/N', fontsize=16)
    # Set axes labels.
    plt.xlabel('Trial folding period (s)', fontsize=16)
    plt.ylabel('Radio frequency (MHz)', fontsize=16)
    # Set tick properties.
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    # Set axes limits.
    plt.gca().set_xlim( (min_period, max_period) )
    plt.gca().set_ylim( (min_freq, max_freq) )
    # Show legend.
    if marker_count>1:
        leg = plt.legend(bbox_to_anchor=(0.0, -0.22, 1.1, 0.1), loc='center', ncol=3, fancybox=True, frameon=True,
                         borderpad=0.3, fontsize=14, handletextpad=0.2, columnspacing=2.0)
        leg.get_frame().set_edgecolor('silver')
    # Set tight layout for figure.    
    plt.tight_layout()
    # Save plot to disk.
    for format in plot_formats:
        plt.savefig(basename + format)
    plt.close()
##########################################################################