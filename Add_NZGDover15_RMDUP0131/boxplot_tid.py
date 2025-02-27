import pandas as pd
import matplotlib.pyplot as plt


data = [
    (1 , 'T01'),
    (2 , 'T02'),
    (3 , 'T03'),
    (4 , 'T04'),
    (5 , 'T05'),
    (6 , 'T06'),
    (7 , 'T07'),
    (8 , 'T08'),
    (9 , 'T09'),
    (10 , 'T10'),
    (11 , 'T11'),
    (12 , 'T12'),
    (13 , 'T13'),
    (14 , 'T14'),
    (15 , 'T15'),
    (16 , 'T16'),
    (255, 'UNDEFINED')
]
df_mapping = pd.DataFrame(data, columns=['tid', 'description'])

df = pd.read_csv('measured_sites.csv')
# Drop rows with NaN values in 'vs30' and 'tid' columns
df = df.dropna(subset=['vs30', 'tid'])

# Map the 'tid' values in the DataFrame to the corresponding values in the created DataFrame
df['tid'] = df['tid'].map(df_mapping.set_index('tid')['description'])


# Create a box plot for 'vs30' grouped by 'gid'
boxplot = df.boxplot(column='vs30', by='tid', figsize=(12, 6), patch_artist=True)

# Calculate the mean values for each group
means = df.groupby('tid')['vs30'].mean()

# Show the plot
plt.suptitle('')  # Suppress the default title to make it cleaner
plt.title('Box plot of vs30 grouped by tid')
plt.xlabel('tid')
plt.xticks(rotation=45)
plt.yscale('log')
plt.yticks([200, 400, 600, 800, 1000, 1200, 1400, 1600])
current_values = plt.gca().get_yticks()
plt.gca().set_yticklabels(['{:.0f}'.format(x) for x in current_values])

plt.ylabel('vs30')
plt.savefig(f'boxplot_tid.png', dpi = 400)
plt.show()
