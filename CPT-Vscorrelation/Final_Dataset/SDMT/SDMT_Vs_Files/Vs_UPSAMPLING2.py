import os
import pandas as pd
import numpy as np

input_folder = './'
output_folder = './output_folder_1.1'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for filename in os.listdir(input_folder):
    if filename.endswith(".csv"):
        print(filename)
        df = pd.read_csv(os.path.join(input_folder, filename))
        depth = df["d"]
        vs = df["vs"]
        max_depth = depth.max()
        depth = pd.concat([pd.Series([0]), depth]).reset_index(drop=True)
        vs = pd.concat([pd.Series([0]), vs]).reset_index(drop=True)
        vs = vs.shift(-1)
        vs.iloc[-1] = vs.iloc[-2]

        # Create a new DataFrame and add 0 to the beginning of the depth column
        df_new = pd.DataFrame()
        depth_new = np.round(np.arange(0.1, max_depth + 0.02, 1), 2) # Add 0 at the beginning of depth_new
        df_new["d"] = depth_new

        # Interpolate the vs values for the new depth array
        df_new["vs"] = np.interp(depth_new, depth, vs)

        original_vs_dict = dict(zip(depth, vs))
        df_new["vs"] = [original_vs_dict.get(d, v) for d, v in zip(depth_new, df_new["vs"])]

        # Ensure originally existed vs values are reserved, creating uniform layers
        for d, v in zip(depth, vs):
            df_new.loc[df_new["d"] >= d, "vs"] = v

        # Append the original depth and vs values to the new DataFrame
        df_original = pd.DataFrame({"d": depth, "vs": vs})
        df_combined = pd.concat([df_new, df_original]).drop_duplicates().sort_values(by="d").reset_index(drop=True)

        # Remove rows with depth values greater than the maximum depth in the original file
        df_combined = df_combined[df_combined["d"] <= max_depth]
        print(df_combined)
        # Save the new DataFrame to a CSV file in the output folder, retaining the original file name
        df_combined.to_csv(os.path.join(output_folder, filename), index=False)