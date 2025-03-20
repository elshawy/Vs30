import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from statsmodels.nonparametric.smoothers_lowess import lowess as sm_lowess
import scipy.interpolate
import scipy.stats

sns.set_style("white")
plt.rc("axes.spines", top=False, right=False)
sns.set_context("paper")

def smooth(x, y, xgrid):
    samples = np.random.choice(len(x), 50, replace=True)
    y_s = y[samples]
    x_s = x[samples]
    y_sm = sm_lowess(y_s, x_s, frac=1./5., it=5, return_sorted=False)
    y_grid = scipy.interpolate.interp1d(x_s, y_sm, fill_value='extrapolate')(xgrid)
    return y_grid

df = pd.read_csv('Stacking_results_downsampled.csv')

# Extract the reference column
x_ax = df['Fs']

for col in df.columns[7:]:
    residuals = df[col]
    xgrid = np.linspace(x_ax.min(), x_ax.max())
    K = 200
    smooths = np.stack([smooth(x_ax, residuals, xgrid) for k in range(K)]).T
    mean = np.nanmean(smooths, axis=1)
    stderr = scipy.stats.sem(smooths, axis=1)
    stderr = np.nanstd(smooths, axis=1, ddof=0)

    # plot
    plt.figure(figsize=(8, 6))
    plt.fill_between(xgrid,mean - 1.96 * stderr, mean + 1.96 * stderr,color='tomato',  alpha=0.25)
    plt.plot(xgrid, mean - 1.96 * stderr, color='red', linestyle='--', alpha=0.8)
    plt.plot(xgrid, mean + 1.96 * stderr, color='red', linestyle='--', alpha=0.8)

    plt.ylim(-3, 3)
    plt.xlim(0.03, 1)
    plt.xscale('log')
    plt.grid(True, alpha=0.3)
    #plt.xticks(np.arange(x_ax.min()*0.9, x_ax.max()*1.1, 4), fontsize=15)
    plt.yticks(fontsize=15)
    plt.plot(x_ax, residuals, '.k', alpha=0.4)
    plt.plot(xgrid, mean, color='w', linestyle='-',linewidth = 3)
    plt.plot(xgrid, mean, color='red', linestyle='-',linewidth = 2, label=col)
    plt.axhline(y=0, color='k', linestyle='--', alpha=0.7)
    plt.xlabel('fs')
    plt.ylabel('Residuals')
    plt.text(0.85, 0.9, f'{col}', fontsize=20, bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.2'),horizontalalignment='left', verticalalignment='top', transform = plt.gca().transAxes)
    plt.text(0.01, 0.99, 'Underprediction', horizontalalignment='left', verticalalignment='top', transform = plt.gca().transAxes, fontsize=13, bbox=dict(facecolor='white', alpha=0.9, edgecolor='None', boxstyle='round,pad=0.2'))
    plt.text(0.01, 0.01, 'Overprediction', horizontalalignment='left', verticalalignment='bottom', transform = plt.gca().transAxes, fontsize=13, bbox=dict(facecolor='white',alpha=0.9,  edgecolor='None', boxstyle='round,pad=0.2'))
#    plt.title(f'ln(Inferred Vs) - ln(Measured Vs)', fontsize=12, style='italic')
    plt.savefig(f'Residuals_{col}.png', dpi=600)
 #   plt.show()
