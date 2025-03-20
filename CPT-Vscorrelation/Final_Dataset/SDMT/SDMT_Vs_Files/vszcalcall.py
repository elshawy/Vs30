from pathlib import Path
from vs_calc import VsProfile, vs30_correlations

# Define the directory containing the files

examples_dir = Path('./')
csv_files = list(examples_dir.glob('SDMT_92532_13.csv'))
total_files = len(csv_files)
for index, file_path in enumerate(csv_files, start=1):
    file_name = file_path.stem
    try:
            # Load the Vs30 profile
        vs_profile = VsProfile.from_file(str(file_path), True)

            # Calculate the VsZ value
        vsz = vs_profile.vsz

            # Calculate the Vs30 value using Boore (2004)
        vs30 = vs30_correlations.boore_2004(vs_profile)
            # Calculate the Vs30 value using Boore (2011)
        vs30_2 = vs30_correlations.boore_2011(vs_profile)

        with open(examples_dir / 'vs30_estimation3.txt', 'a') as output_file:
                output_file.write(f"{file_name}, {vs_profile.max_depth:.2f}, {vsz:.2f}, {vs30[0]:.2f},{vs30[1]:.2f}\n")

    except Exception as e:
        with open(examples_dir / 'error3.txt', 'a') as error_file:
            error_file.write(f"Error processing {file_name}: {str(e)}\n")
    print(f'Done ({index}/{total_files})')
