import os
import csv
import pandas as pd

def merge_csv_files():
    input_folder = "input"
    output_folder = "output"
    merged_data = pd.DataFrame()

    # Read the address.csv file to get the building numbers (No)
    address_file = os.path.join(input_folder, "address.csv")
    building_numbers = {}
    with open(address_file, "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            No, name, _, _ = row
            building_numbers[name] = No

    # Iterate over CSV files in the output folder
    for filename in os.listdir(output_folder):
        if filename.endswith(".csv"):
            filepath = os.path.join(output_folder, filename)
            df = pd.read_csv(filepath, encoding="shift_jis")

            building_name = os.path.splitext(filename)[0]
            building_no = building_numbers.get(building_name, "")
            df.insert(1, "No", building_no)  # Insert the building number column
            merged_data = merged_data.append(df, ignore_index=True)

    # Define the desired header order
    desired_header = [
        "建物名",
        "No",
        "30年で震度5弱以上となる確率",
        "30年で震度5強以上となる確率",
        "30年で震度6弱以上となる確率",
        "30年で震度6強以上となる確率"
    ]

    # Reorder columns in the merged data
    merged_data = merged_data[desired_header]

    # Write merged data to an Excel file with Shift_JIS encoding
    merged_filename = os.path.join(output_folder, "merged_data.xlsx")
    merged_data.to_excel(merged_filename, index=False, encoding="shift_jis")

    print("CSV files merged and exported to Excel successfully.")

# Call the function to merge and export the CSV files to Excel
merge_csv_files()
