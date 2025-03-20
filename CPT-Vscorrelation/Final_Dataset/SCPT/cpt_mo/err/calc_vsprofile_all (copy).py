from pathlib import Path
from vs_calc import CPT, VsProfile, vs30_correlations

examples_dir = Path('./')

# Open the output file and write the header
with open(examples_dir / 'vs30_estimation_Final.txt', 'w') as output_file:
    output_file.write(
        "File Name, max_depth of CPT, Vsz_Hegazy 2006, Vs30_Boore 2004, Vsz_Andrus 2007-H, Vs30_Boore 2004, Vsz_Andrus 2007-P, Vs30_Boore 2004, Vsz_Robertson 2009, Vs30_Boore 2004, Vsz_McGann 2015, Vs30_Boore 2004,Vsz_McGann 2018, Vs30_Boore 2004\n")

for file_path in examples_dir.glob('*.csv'):
    file_name = file_path.stem
    try:
        cpt = CPT.from_file(str(file_path))

        # CPT-Vs Correlations
        vs_correlations = "hegazy_2006"
        vs_correlations2 = "andrus_2007"
        vs_correlations3 = "andrus_2007_2"
        vs_correlations4 = "robertson_2009"`
        vs_correlations5 = "mcgann_2015"
        vs_correlations6 = "mcgann_2018"

        # Create VsProfile objects from the CPT file
        vs_profile = VsProfile.from_cpt(cpt, vs_correlations)
        vs_profile2 = VsProfile.from_cpt(cpt, vs_correlations2)
        vs_profile3 = VsProfile.from_cpt(cpt, vs_correlations3)
        vs_profile4 = VsProfile.from_cpt(cpt, vs_correlations4)
        vs_profile5 = VsProfile.from_cpt(cpt, vs_correlations5)
        vs_profile6 = VsProfile.from_cpt(cpt, vs_correlations6)

        # Calculate Vs30 values
        vs30_1 = vs30_correlations.boore_2004(vs_profile)[0]
        vs30_2 = vs30_correlations.boore_2004(vs_profile2)[0]
        vs30_3 = vs30_correlations.boore_2004(vs_profile3)[0]
        vs30_4 = vs30_correlations.boore_2004(vs_profile4)[0]
        vs30_5 = vs30_correlations.boore_2004(vs_profile5)[0]
        vs30_6 = vs30_correlations.boore_2004(vs_profile6)[0]
      

        # Write the results to the output file
        with open(examples_dir / 'vs30_estimation_Final.txt', 'a') as output_file:
            output_file.write(
                f"{file_name}, {vs_profile.max_depth:.2f}, {vs_profile.vsz:.2f}, {vs30_1:.2f}, {vs_profile2.vsz:.2f}, {vs30_2:.2f}, {vs_profile3.vsz:.2f}, {vs30_3:.2f}, {vs_profile4.vsz:.2f}, {vs30_4:.2f}, {vs_profile5.vsz:.2f}, {vs30_5:.2f}, {vs_profile6.vsz:.2f}, {vs30_6:.2f}\n")


    except Exception as e:
        with open(examples_dir / 'vs30_estimation_Final.txt', 'a') as output_file:
            output_file.write(
                f"{file_name},N,N,N,N,N,N,N,N,N,N,N,N,N\n")
    print('Done')
