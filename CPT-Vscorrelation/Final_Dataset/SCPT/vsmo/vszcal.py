from pathlib import Path
from vs_calc import VsProfile, vs30_correlations

# Define the directory containing the files
examples_dir = Path('./')

# Open a text file to write the output
with open(examples_dir / 'output.txt', 'w') as output_file:
    # Iterate over all CSV files in the directory
    for file_path in examples_dir.glob('*.csv'):
        file_name = file_path.name

        # Load the Vs30 profile
        vs_profile = VsProfile.from_file(str(file_path), True)

        # Calculate the VsZ value
        vsz = vs_profile.vsz
        output_file.write(f"{file_name}, {vs_profile.max_depth:.2f}, {vsz:.2f} m/s \n")

