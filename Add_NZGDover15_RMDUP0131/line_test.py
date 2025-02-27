import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Create DataFrames from the given list of tuples
data = [
    (0, '00_water'),
    (1, '01_peat'),
    (2, '04_fill'),
    (3, '05_fluvialEstuarine'),
    (4, '06_alluvium'),
    (5, '08_lacustrine'),
    (6, '09_beachBarDune'),
    (7, '10_fan'),
    (8, '11_loess'),
    (9, '12_outwash'),
    (10, '13_floodplain'),
    (11, '14_moraineTill'),
    (12, '15_undifSed'),
    (13, '16_terrace'),
    (14, '17_volcanic'),
    (15, '18_crystalline'),
    (255, 'NO DATA')
]
df_mapping = pd.DataFrame(data, columns=['gid', 'description'])

data2 = [
    (1 , 'T01'),
    (2 , 'T02'),
    (3 , 'T03'),
    (4 , 'T04'),
    (5 , 'T05'),
    (6 , 'T06'),
    (7 , 'T07'),
    (8 , 'T08'),
    (9 , 'T09'),
    (0 , 'T10'),
    (11 , 'T11'),
    (12 , 'T12'),
    (13 , 'T13'),
    (14 , 'T14'),
    (15 , 'T15'),
    (16 , 'T16'),
    (255, 'NO DATA')
]
df_mapping2 = pd.DataFrame(data2, columns=['tid', 'description'])

# Read the CSV file
df = pd.read_csv('measured_sites.csv')

# Drop rows with NaN values in 'vs30' and 'gid' columns
df = df.dropna(subset=['vs30', 'gid'])

# Map the 'gid' values in the DataFrame to the corresponding values in the created DataFrame
df['gid'] = df['gid'].map(df_mapping.set_index('gid')['description'])

# Exclude the '00_water' group from the DataFrame
df = df[df['gid'] != '00_water']

# Calculate the median, standard deviation, and count for each group using the log function
grouped = df.groupby('gid')['vs30']
medians = grouped.apply(lambda x: np.exp(np.median(np.log(x))))
stds = grouped.apply(lambda x: np.std(np.log(x)))
counts = grouped.size()
stds[stds == 0] = 0.5

# Convert the standard deviation from log scale to linear scale
stds2 = medians * (np.exp(stds) - 1)

# Create a numpy array with the given data
data_array = np.array([
    [1, 162.892120019443, 0.301033220758108],
    [2, 272.512711921894, 0.280305955290694],
    [3, 199.502400319993, 0.438753673163297],
    [4, 271.050623687222, 0.243486579272276],
    [5, 326, 0.5],
    [6, 204.373998521848, 0.232196981798137],
    [7, 246.6138371423, 0.344601218802256],
    [8, 472.749388885179, 0.354562104171167],
    [9, 399, 0.5],
    [10, 197.472849225266, 0.202629769603115],
    [11, 453, 0.512],
    [12, 455, 0.545],
    [13, 335.279503497185, 0.602886888230288],
    [14, 635, 0.995],
    [15, 690.974348966211, 0.446036993981441]
])

# Extract the group, mean, and standard deviation from the numpy array
groups = data_array[:, 0]
means = data_array[:, 1]
stds_array = data_array[:, 2]

# Calculate means + 1std and means - 1std
means_plus_1std = np.exp(stds_array) * means
means_minus_1std = np.exp(-stds_array) * means

# Calculate the error bars
yerr = [means - means_minus_1std, means_plus_1std - means]

medians_plus_1std = np.exp(stds) * medians
medians_minus_1std = np.exp(-stds) * medians

# Calculate the error bars
yerr2 = [medians - medians_minus_1std, medians_plus_1std - medians]

# Ensure the lengths of medians and stds match
stds = stds.reindex(medians.index)

# Plot the median and +-std for each group from the DataFrame
plt.figure(figsize=(12, 6))
plt.errorbar(np.arange(len(medians)) + 0.2, medians, yerr=yerr2, fmt='o', capsize=5, label='Median ± 1 std (Current Dataset)', color='red')

# Plot the mean and +-std for each group from the numpy array
plt.errorbar(np.arange(len(groups)) - 0.2, means, yerr=yerr, fmt='o', capsize=5, label='Mean ± 1 std (Posterior Model)')

# Plot a scatter plot for each gid and vs30, shifting the gid values by 0.2 to the right and adding the scatter label once
scatter_label = 'Current Vs30 Data'
for i, gid in enumerate(medians.index):
    subset = df[df['gid'] == gid]
    plt.scatter([i] * len(subset), subset['vs30'], color='grey', label=scatter_label if i == 0 else None)

# Check if the data and error bars are the same
print(f'Medians: {medians}')
print(f'Standard Deviations: {stds}')
print(f'Means: {means}')
print(f'Standard Deviations (Array): {stds_array}')

# Customize the plot
plt.title('Comparison of Median and Mean ±1 std of vs30 grouped by gid')
plt.xlabel('gid')
plt.ylabel('vs30')
xtick_labels = ['G01', 'G04', 'G05', 'G06', 'G08', 'G09', 'G10', 'G11', 'G12', 'G13', 'G14', 'G15', 'G16', 'G17', 'G18', 'UNDEFINED DATA']

plt.xticks(ticks=np.arange(len(medians)), labels=xtick_labels, rotation=45)  # Rotate x-ticks by 90 degrees
plt.legend()
plt.yscale('log')
plt.yticks([200, 400, 600, 800, 1000, 1200, 1400, 1600])
current_values = plt.gca().get_yticks()
plt.gca().set_yticklabels(['{:.0f}'.format(x) for x in current_values])
output_df = pd.DataFrame({'Median': medians, 'Std Dev': stds, 'Count': counts})
output_df.to_csv('medians_stds_gidtes.txt', sep='\t', index=True)

plt.grid(True)  # Add grid lines
plt.tight_layout()
plt.savefig('lineplot_gid_Compartes.png', dpi=400)
plt.show()