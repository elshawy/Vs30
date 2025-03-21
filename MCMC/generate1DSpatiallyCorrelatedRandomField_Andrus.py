import numpy as np
import os
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from vs_calc import VsProfile, vs30_correlations

def generate_spatially_correlated_field(depths, num_realizations, correlation_length, mean, std_dev):
    num_points = len(depths)
    correlation_matrix = np.exp(-np.abs(np.subtract.outer(depths, depths)) / correlation_length)
    L = np.linalg.cholesky(correlation_matrix)
    uncorrelated_random_fields = np.random.randn(num_realizations, num_points)
    std_dev_ln = np.sqrt(np.log(1 + (std_dev / mean) ** 2))
    correlated_fields_ln = std_dev_ln * (uncorrelated_random_fields @ L.T)
    return correlated_fields_ln

filename = 'SCPT_195188.csv'
data = pd.read_csv(filename, usecols=['Depth', 'Andrus-P Vs'])
depth_interval_csv = np.diff(data['Depth']).mean()
depths = np.linspace(0, 30, 3001)
mean_vs = np.interp(depths, data['Depth'], data['Andrus-P Vs'])
random_fields_ln = generate_spatially_correlated_field(depths, num_realizations=1000, correlation_length=250, mean=mean_vs, std_dev=45)
matched_random_fields_ln = np.array([np.interp(data['Depth'], depths, random_fields_ln[i, :]) for i in range(random_fields_ln.shape[0])]).T
matched_data_ln = pd.DataFrame(matched_random_fields_ln, columns=[f'Random_Field_{i}' for i in range(random_fields_ln.shape[0])])
matched_data_ln['Depth'] = data['Depth']
merged_data = pd.merge(data, matched_data_ln, on='Depth')

for i in range(random_fields_ln.shape[0]):
    merged_data[f'Andrus-P Vs_{i}'] = merged_data['Andrus-P Vs'] * np.exp(merged_data[f'Random_Field_{i}'])
merged_data = merged_data.drop(columns=merged_data.filter(like='Random_Field_').columns)

min_values = merged_data.drop(columns=['Depth']).min(axis=1)
max_values = merged_data.drop(columns=['Depth']).max(axis=1)
min_array = np.column_stack((merged_data['Depth'], min_values))
max_array = np.column_stack((merged_data['Depth'], max_values))
data_origin = pd.read_csv('SCPT_195188.csv', usecols=['Depth', 'Andrus-P Vs'])

plt.figure(figsize=(6, 10))
plt.plot(min_array[:, 1], min_array[:, 0], color='grey', linestyle='--', label='Minimum Values')
plt.plot(max_array[:, 1], max_array[:, 0], color='grey', linestyle='--', label='Maximum Values')
plt.plot(data_origin['Andrus-P Vs'], data_origin['Depth'], color='red', label='Original Data')
plt.xlabel('Andrus-P Vs')
plt.ylabel('Depth (m)')
plt.title('Minimum and Maximum Values Plot')
plt.gca().invert_yaxis()
plt.legend()
plt.xlim(0, 1000)
plt.savefig('min_max_values_plot.png')
plt.show()
plt.close()

save_path = f'vs_profiles for {filename}'
os.makedirs(save_path, exist_ok=True)

for col in merged_data.columns:
    if col != 'Depth':
        output_df = merged_data[['Depth', col]]
        output_df.columns = ['d', 'vs']
        output_df.to_csv(os.path.join(save_path, f'depth_vs_{col}.csv'), index=False)
        print(f'Saved {os.path.join(save_path, f"depth_vs_{col}.csv")}')

examples_dir = Path(save_path)
result_file_path = examples_dir / 'vsz_estimation.csv'
if os.path.exists(result_file_path):
    os.remove(result_file_path)

for file_path in examples_dir.glob('*.csv'):
    file_name = file_path.stem
    try:
        vs_profile = VsProfile.from_file(file_path, file_name, layered=False)
        vsz = vs_profile.calc_vsz()
    except Exception as e:
        print(f"Error processing {file_name}: {e}")
        continue

    with open(result_file_path, 'a') as output_file:
        output_file.write(f"{file_name},{vsz}\n")

vsz_data = pd.read_csv(f'vs_profiles for {filename}/vsz_estimation.csv', header=None, names=['File', 'Vsz'])
plt.hist(vsz_data['Vsz'], bins=30)
std = np.log(vsz_data['Vsz']).std()
plt.text(0.5, 0.5, f"Standard Deviation of Vsz values: {std}", horizontalalignment='center', verticalalignment='center', transform=plt.gca().transAxes)
print(f"Standard Deviation of Vsz values: {std}")

plt.xlabel('Vsz (m/s)')
plt.ylabel('Counts')
plt.title('Vsz Histogram')
plt.savefig('vsz_histogram.png')