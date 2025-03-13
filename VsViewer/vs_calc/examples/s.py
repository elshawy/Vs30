from pathlib import Path
from vs_calc import VsProfile, vs30_correlations
file_name = 'SCPT_170538.csv'
# Load the Vs30 profile
vs_profile = VsProfile.from_file(file_name, True)

# Calculate the VsZ value
vsz = vs_profile.vsz
print(file_name + f' Vsz = {vsz:.2f} m/s')
# Calculate the Vs30 value
vs30 = vs30_correlations.boore_2011(vs_profile)
print(f'Based on Boore (2011) Vs30 = {vs30[0]:.2f} m/s and sigma = {vs30[1]:.2f}')
vs302 = vs30_correlations.boore_2004(vs_profile)
print(f'Based on Boore (2004) Vs30 = {vs302[0]:.2f} m/s and sigma = {vs302[1]:.2f}')

