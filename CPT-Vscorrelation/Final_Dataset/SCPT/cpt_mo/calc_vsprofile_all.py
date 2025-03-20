from pathlib import Path
from vs_calc import CPT, VsProfile, vs30_correlations

examples_dir = Path('./')

for file_path in examples_dir.glob('*.csv'):
    file_name = file_path.stem
    cpt = CPT.from_file(str(file_path))

    # CPT-Vs Correlations
    vs_correlations = "hegazy_2006"
    vs_correlations2 = "andrus_2007_H"
    vs_correlations3 = "andrus_2007_P"
    vs_correlations4 = "robertson_2009"
    vs_correlations5 = "mcgann_2015"
    vs_correlations6 = "mcgann_2018"

    # Create VsProfile objects from the CPT file
    vs_profile = VsProfile.from_cpt(cpt, vs_correlations)
    vs_profile2 = VsProfile.from_cpt(cpt, vs_correlations2)
    vs_profile3 = VsProfile.from_cpt(cpt, vs_correlations3)
    vs_profile4 = VsProfile.from_cpt(cpt, vs_correlations4)
    vs_profile5 = VsProfile.from_cpt(cpt, vs_correlations5)
    vs_profile6 = VsProfile.from_cpt(cpt, vs_correlations6)
    # Extract depth and vs values
    depth, vs = vs_profile.depth, vs_profile.vs
    depth2, vs2 = vs_profile2.depth, vs_profile2.vs
    depth3, vs3 = vs_profile3.depth, vs_profile3.vs
    depth4, vs4 = vs_profile4.depth, vs_profile4.vs
    depth5, vs5 = vs_profile5.depth, vs_profile5.vs
    depth6, vs6 = vs_profile6.depth, vs_profile6.vs
    # Create an output file for each input file
    with open(examples_dir / f'{file_name}_result.txt', 'w') as output_file:
        # Write the header row
        output_file.write("File Name, Depth, Hegazy Vs, Andrus-H Vs, Andrus-P Vs, Rob Vs, Mc15 Vs,  Mc18 Vs\n")

        # Write the output to the file
        for d, v,  v2, v3,  v4, v5, v6 in zip(depth, vs,  vs2,  vs3,  vs4,  vs5, vs6):
            output_file.write(f"{file_name}, {d:.2f}, {v:.2f},  {v2:.2f},  {v3:.2f}, {v4:.2f},  {v5:.2f}, {v6:.2f}\n")
        print('Done')