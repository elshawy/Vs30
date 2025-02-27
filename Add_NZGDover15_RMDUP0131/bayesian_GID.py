import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
from vs30 import model, model_geology, sites_cluster

geo_ids = {
    1: ("G01", "Peat"),
    2: ("G04", "Artificial fill"),
    3: ("G05", "Fluvial and estuarine deposits"),
    4: ("G06", "Alluvium and valley sediments"),
    5: ("G08", "Lacustrine"),
    6: ("G09", "Beach, bar, dune deposits"),
    7: ("G10", "Fan deposits"),
    8: ("G11", "Loess"),
    9: ("G12", "Glacigenic sediments"),
    10: ("G13", "Flood deposits"),
    11: ("G14", "Glacial moraines and till"),
    12: ("G15", "Undifferentiated sediments and sedimentary rocks"),
    13: ("G16", "Terrace deposits and old alluvium"),
    14: ("G17", "Volcanic rocks and deposits"),
    15: ("G18", "Crystalline rocks"),
}

df = pd.read_csv('measured_sites.csv')
print(df)

vs30_geo_id_df = df.copy()
vs30_geo_id_df = vs30_geo_id_df.loc[vs30_geo_id_df['gid'] != 255]  # remove 255 = ID_NODATA
vs30_geo_id_df = vs30_geo_id_df.loc[vs30_geo_id_df['gid'] != 0]  # remove 0 = Water

means = []
errors = []
for i, (gid, geo_name) in geo_ids.items():
    print(gid, geo_name)
    count = vs30_geo_id_df.loc[vs30_geo_id_df['gid'] == i].Vs30.count()
    vs30_mean = vs30_geo_id_df.loc[vs30_geo_id_df['gid'] == i].Vs30.mean()
    vs30_std = vs30_geo_id_df.loc[vs30_geo_id_df['gid'] == i].Vs30.std()
    print("n = {} vs30={} std= {}".format(count, vs30_mean, vs30_std))

    means.append(vs30_mean)
    errors.append(vs30_std)

prior = model_geology.model_prior()
prior_means = prior.T[0]
prior_errors = prior.T[1] * prior_means

posterior = model_geology.model_posterior_paper()
print(posterior)
posterior_means = posterior.T[0]

means_plus_1std = posterior_means * (np.exp(posterior.T[1]) - 1)
means_minus_1std = posterior_means * (1 - np.exp(-posterior.T[1]))
yerr2 = [means_minus_1std, means_plus_1std]
print(means_plus_1std)
print(means_minus_1std)
print(yerr2)

vs30_geo_id_df = vs30_geo_id_df.rename(columns={"NZTM_X": "easting", "NZTM_Y": "northing", "Vs30": "vs30"})
new_posterior = model.posterior(posterior, vs30_geo_id_df, "gid")
new_posterior_means = new_posterior.T[0]
new_posterior_errors = new_posterior.T[1] * new_posterior_means
upper_new_posterior_errors = new_posterior_errors + new_posterior_means
lower_new_posterior_errors = new_posterior_means - new_posterior_errors

# Correctly calculate the error bars
means_plus_1std2 = new_posterior_means * (np.exp(new_posterior.T[1]) - 1)
means_minus_1std2 = new_posterior_means * (1 - np.exp(-new_posterior.T[1]))
yerr = [means_minus_1std2, means_plus_1std2]

median_vs30 = np.median(new_posterior[:, 0])
print(new_posterior_means)
print(upper_new_posterior_errors)
print(lower_new_posterior_errors)

plt.figure(figsize=(12, 6))
scatter_label = 'Current Vs30 Data'
for i, (gid, geo_name) in enumerate(geo_ids.items()):
    subset = vs30_geo_id_df[vs30_geo_id_df['gid'] == gid]
    plt.scatter([i] * len(subset), subset['vs30'], color='grey', label=scatter_label if i == 0 else None)

posterior = model_geology.model_posterior_paper()
posterior_means = posterior.T[0]
means_plus_1std = posterior_means * (np.exp(posterior.T[1]) - 1)
means_minus_1std = posterior_means * (1 - np.exp(-posterior.T[1]))
yerr2 = [means_minus_1std, means_plus_1std]
plt.errorbar(np.arange(len(posterior_means)) - 0.2, posterior_means, yerr=yerr2, fmt='o', capsize=5, label='Median ± 1 std (Foster)', color='blue')

# Plot the median values for new_posterior
plt.errorbar(np.arange(len(new_posterior_means))+0.2, new_posterior_means, yerr=yerr, fmt='o', capsize=5, label='Median ± 1 std (New Posterior)', color='r')
plt.title('Comparison of Median and Mean ±1 std of vs30 grouped by gid')
plt.xlabel('gid')
plt.ylabel('vs30')
xtick_labels = ['G01', 'G04', 'G05', 'G06', 'G08', 'G09', 'G10', 'G11', 'G12', 'G13', 'G14', 'G15', 'G16', 'G17', 'G18']

plt.xticks(ticks=np.arange(len(new_posterior_means)), labels=xtick_labels, rotation=45)  # Rotate x-ticks by 90 degrees
plt.legend()
plt.yscale('log')
plt.yticks([200, 400, 600, 800, 1000, 1200, 1400, 1600])
current_values = plt.gca().get_yticks()
plt.gca().set_yticklabels(['{:.0f}'.format(x) for x in current_values])
print(posterior)
print(new_posterior)
plt.grid(True)  # Add grid lines
plt.tight_layout()
plt.show()