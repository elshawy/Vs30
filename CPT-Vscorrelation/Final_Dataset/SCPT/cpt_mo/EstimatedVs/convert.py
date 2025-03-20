import os
import shutil

# Define the input and output folders
input_folder = './'
output_folder = './output_folder'

# List of numbers to check in file names
numbers = [
    "14526", "14538", "14539", "14540", "14541", "14543", "14548", "14550", "14552", "14556",
    "14651", "36413", "57279", "57280", "57339", "57341", "57342", "57343", "57345", "57346",
    "57347", "57348", "57349", "57350", "57351", "57353", "57354", "57355", "57356", "57357",
    "57358", "57359", "57360", "57362", "57363", "57364", "57365", "57366", "61758", "94658",
    "114319", "114322", "124801", "124802", "125043", "126232", "128450", "136515", "140250",
    "140251", "140253", "140254", "140257", "140260", "140262", "140263", "148992", "148995",
    "148998", "148999", "154032", "154771", "154775", "156296", "156298", "156300", "156301",
    "156307", "156308", "156310", "156311", "165738", "165739", "182797", "184148", "192457",
    "192465", "192469", "192473", "192478", "192480", "192483", "195188", "195941", "196093",
    "205817", "205818", "217000"
]

# Create the output folder if it does not exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Iterate through the files in the input folder
for filename in os.listdir(input_folder):
    # Check if any of the numbers are in the file name
    if any(number in filename for number in numbers):
        # Move the file to the output folder
        shutil.move(os.path.join(input_folder, filename), os.path.join(output_folder, filename))
        print(f"Moved file: {filename}")