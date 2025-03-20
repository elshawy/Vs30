import pandas as pd
from pathlib import Path
from vs_calc import CPT, VsProfile, vs30_correlations

examples_dir = Path('./')

for file_path in examples_dir.glob('*.csv'):
    file_name = file_path.stem
    cpt = CPT.from_file(str(file_path))

    # Round depth values in the CPT object to two decimal places
    cpt.depth = cpt.depth.round(2)

    # CPT-Vs Correlations
    vs_correlations = "hegazy_2006"
    vs_correlations2 = "andrus_2007_H"
    vs_correlations3 = "andrus_2007_P"
    vs_correlations4 = "robertson_2009"
    vs_correlations5 = "mcgann_2015"
    vs_correlations6 = "mcgann_2018"

    # Create VsProfile objects from the rounded CPT file
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

    # Read the input CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Round the first column values to two decimal places
    df.iloc[:, 0] = df.iloc[:, 0].round(2)

    # Create a DataFrame for the Vs correlations
    vs_df = pd.DataFrame({
        'Depth': depth,
        'Hegazy Vs': vs,
        'Andrus-H Vs': vs2,
        'Andrus-P Vs': vs3,
        'Rob Vs': vs4,
        'Mc15 Vs': vs5,
        'Mc18 Vs': vs6
    })

    # Merge the original DataFrame with the Vs correlations DataFrame
    df = pd.merge(df, vs_df, how='left', left_on='Depth', right_on='Depth')

    # Save the DataFrame to a new CSV file
    df.to_csv(examples_dir / f'{file_name}_result.csv', index=False)
    print('Done')