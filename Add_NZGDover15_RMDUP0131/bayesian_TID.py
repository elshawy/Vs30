import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
from vs30 import model, model_terrain, sites_cluster

terrain_ids = {
    1: ("T01", "T01"),
    2: ("T02", "T02"),
    3: ("T03", "T03"),
    4: ("T04", "T04"),
    5: ("T05", "T05"),
    6: ("T06", "T06"),
    7: ("T07", "T07"),
    8: ("T08", "T08"),
    9: ("T09", "T09"),
    10: ("T10", "T10"),
    11: ("T11", "T11"),
    12: ("T12", "T12"),
    13: ("T13", "T13"),
    14: ("T14", "T14"),
    15: ("T15", "T15"),
    16: ("T16", "T16"),
}

df = pd.read_csv('measured_sites.csv')
print(df)

vs30_terrain_id_df = df.copy()
vs30_terrain_id_df = vs30_terrain_id_df.loc[vs30_terrain_id_df['tid'] != 255]  # remove 255 = ID_NODATA

means = []
errors = []
for i, (tid, tid_name) in terrain_ids.items():
    print(tid, tid_name)
    count = vs30_terrain_id_df.loc[vs30_terrain_id_df['tid'] == i].Vs30.count()
    vs30_mean = vs30_terrain_id_df.loc[vs30_terrain_id_df['tid'] == i].Vs30.mean()
    vs30_std = vs30_terrain_id_df.loc[vs30_terrain_id_df['tid'] == i].Vs30.std()
    print("n = {} vs30={} std= {}".format(count, vs30_mean, vs30_std))

    means.append(vs30_mean)
    errors.append(vs30_std)

prior = model_terrain.model_prior()
prior_means = prior.T[0]
prior_errors = prior.T[1] * prior_means

posterior = model_terrain.model_posterior_paper()
print(posterior)
posterior_means = posterior.T[0]

means_plus_1std = posterior_means * (np.exp(posterior.T[1]) - 1)
means_minus_1std = posterior_means * (1 - np.exp(-posterior.T[1]))
yerr2 = [means_minus_1std, means_plus_1std]
print(means_plus_1std)
print(means_minus_1std)
print(yerr2)

vs30_terrain_id_df = vs30_terrain_id_df.rename(columns={"NZTM_X": "easting", "NZTM_Y": "northing", "Vs30": "vs30"})
new_posterior = model.posterior(posterior, vs30_terrain_id_df, "tid")
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
for i, (tid, tid_name) in enumerate(terrain_ids.items()):
    subset = vs30_terrain_id_df[vs30_terrain_id_df['tid'] == tid]
    plt.scatter([i] * len(subset), subset['vs30'], color='grey', label=scatter_label if i == 0 else None)

posterior = model_terrain.model_posterior_paper()
posterior_means = posterior.T[0]
means_plus_1std = posterior_means * (np.exp(posterior.T[1]) - 1)
means_minus_1std = posterior_means * (1 - np.exp(-posterior.T[1]))
yerr2 = [means_minus_1std, means_plus_1std]
plt.errorbar(np.arange(len(posterior_means)) - 0.2, posterior_means, yerr=yerr2, fmt='o', capsize=5, label='Median ± 1 std (Foster)', color='blue')

# Plot the median values for new_posterior
plt.errorbar(np.arange(len(new_posterior_means))+0.2, new_posterior_means, yerr=yerr, fmt='o', capsize=5, label='Median ± 1 std (New Posterior)', color='r')
plt.title('Comparison of Median and Mean ±1 std of vs30 grouped by tid')
plt.xlabel('tid')
plt.ylabel('vs30')
xtick_labels = ['T01', 'T02', 'T03', 'T04', 'T05', 'T06', 'T07', 'T08', 'T09', 'T10', 'T11', 'T12', 'T13', 'T14', 'T15', 'T16']

plt.xticks(ticks=np.arange(len(xtick_labels)), labels=xtick_labels, rotation=45)  # Rotate x-ticks by 45 degrees
plt.legend()
plt.yscale('log')
plt.yticks([200, 400, 600, 800, 1000, 1200, 1400, 1600])
current_values = plt.gca().get_yticks()
plt.gca().set_yticklabels(['{:.0f}'.format(x) for x in current_values])
print(posterior)
print(new_posterior)
plt.grid(True)  # Add grid lines
plt.tight_layout()
plt.savefig('Updated_TID.png',dpi=400)
plt.show()
