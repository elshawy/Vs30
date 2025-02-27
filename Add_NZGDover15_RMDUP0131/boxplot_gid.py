import pandas as pd
import matplotlib.pyplot as plt


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
    (255, 'UNDEFINED')
]
df_mapping = pd.DataFrame(data, columns=['gid', 'description'])

df = pd.read_csv('measured_sites.csv')
# Drop rows with NaN values in 'vs30' and 'tid' columns
df = df.dropna(subset=['vs30', 'gid'])

# Map the 'tid' values in the DataFrame to the corresponding values in the created DataFrame
df['gid'] = df['gid'].map(df_mapping.set_index('gid')['description'])


# Create a box plot for 'vs30' grouped by 'gid'
boxplot = df.boxplot(column='vs30', by='gid', figsize=(12, 6), patch_artist=True)

# Calculate the mean values for each group
means = df.groupby('gid')['vs30'].mean()

# Show the plot
plt.suptitle('')  # Suppress the default title to make it cleaner
plt.title('Box plot of vs30 grouped by gid')
plt.xlabel('gid')
plt.xticks(rotation=45)
plt.yscale('log')
plt.yticks([200, 400, 600, 800, 1000, 1200, 1400, 1600])
current_values = plt.gca().get_yticks()
plt.gca().set_yticklabels(['{:.0f}'.format(x) for x in current_values])

plt.ylabel('vs30')
plt.tight_layout()
plt.savefig(f'boxplot_gid.png', dpi = 400)
plt.show()
