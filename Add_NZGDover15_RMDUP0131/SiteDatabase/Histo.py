import os
import pandas as pd
import matplotlib.pyplot as plt

folder_path = './'
bin_intervals = range(0, 1100, 100)

for file_name in os.listdir(folder_path):
    if file_name.endswith('.csv'):
        file_path = os.path.join(folder_path, file_name)
        df = pd.read_csv(file_path, delimiter=',')
        if 'Vs30' in df.columns:
            plt.figure()
            plt.figszie = (10, 5)
            counts, bins, patches = plt.hist(df['Vs30'], bins=bin_intervals, edgecolor='black')
            plt.title(f'Histogram of Vs30 for {file_name}')
            plt.xlabel('Vs30')
            plt.ylabel('Counts')
            plt.grid(True, alpha=0.5)

            # Calculate standard deviation, median, and total counts
            std_dev = df['Vs30'].std()
            med = df['Vs30'].median()
            total_counts = df['Vs30'].count()

            # Annotate total counts and standard deviation
            plt.text(0.95, 0.65, f'Median: {med:.2f}\nStd Dev: {std_dev:.2f}\nTotal: {total_counts}',
                     transform=plt.gca().transAxes, ha='right', va='top',
                     bbox=dict(facecolor='white', alpha=0.5))

            # Add a vertical line for the median and include it in the legend
            plt.axvline(med, color='red', linestyle='--', linewidth=2, label='Median')
            plt.legend()

            plt.savefig(f'{file_name}_Vs30_histogram.png')
            plt.close()
        else:
            print(f"File {file_name} does not contain 'Vs30' column")