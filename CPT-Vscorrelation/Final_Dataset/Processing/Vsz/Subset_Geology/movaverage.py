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

df = pd.read_csv('R09forall.csv')

# Extract the reference column
depth = df.iloc[:, 0]

for col in df.columns[1:]:
    residuals = df[col]
    xgrid = np.linspace(depth.min(), depth.max())
    K = 200
    smooths = np.stack([smooth(depth, residuals, xgrid) for k in range(K)]).T
    mean = np.nanmean(smooths, axis=1)
    stderr = scipy.stats.sem(smooths, axis=1)
    stderr = np.nanstd(smooths, axis=1, ddof=0)

    # plot
    plt.figure(figsize=(8, 6))
    #plt.fill_between(xgrid,mean - 1.96 * stderr, mean + 1.96 * stderr,color='tomato',  alpha=0.25)
    #plt.plot(xgrid, mean - 1.96 * stderr, color='red', linestyle='--', alpha=0.8)
    #plt.plot(xgrid, mean + 1.96 * stderr, color='red', linestyle='--', alpha=0.8)

    plt.ylim(-1.5, 1.5)
    plt.xlim(13.5, 30.5)
    plt.grid(True, alpha=0.2)

    plt.plot(depth, residuals, linestyle = 'None', markersize=12, color = 'r', marker ='o', markeredgecolor='k', alpha=0.8)

    #plt.plot(xgrid, mean, color='red', linestyle='--',linewidth = 2, label=col)
    plt.axhline(y=0, color='k', linestyle='--', alpha=0.7)
    plt.xticks(np.arange(14,30,3), fontsize=15)
    plt.yticks([-1.5,-1,-0.5,0,0.5,1,1.5,], fontsize=15)
    plt.text(28.5, 1.35, f'{col}', fontsize=20, bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.2'))
    plt.text(0.01, 0.99, 'Underprediction', horizontalalignment='left', verticalalignment='top', transform = plt.gca().transAxes, fontsize=15, bbox=dict(facecolor='white', alpha=0.9, edgecolor='None', boxstyle='round,pad=0.2'))
    plt.text(0.01, 0.01, 'Overprediction', horizontalalignment='left', verticalalignment='bottom', transform = plt.gca().transAxes, fontsize=15, bbox=dict(facecolor='white',alpha=0.9,  edgecolor='None', boxstyle='round,pad=0.2'))
#    plt.title(f'ln(Inferred Vs) - ln(Measured Vs)', fontsize=12, style='italic')
    plt.xlabel('Depth', fontsize=13)
    plt.ylabel('Residuals', fontsize=13)
    #plt.title(f'ln(Inferred VsZ) - ln(Measured VsZ)', fontsize=12, style='italic')
    plt.savefig(f'{col} Residuals_movingavg_outchch_H.png', dpi=600)
    #plt.show()