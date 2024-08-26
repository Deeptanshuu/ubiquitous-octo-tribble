import pandas as pd

def replace_ampersand_in_names(csv_file):
    # Read the CSV file
    recipes_data = pd.read_csv(csv_file)

    # Check if 'name' column exists
    if 'name' in recipes_data.columns:
        # Replace '&' with 'and' in the 'name' column
        recipes_data['name'] = recipes_data['name'].str.replace('&', 'and', regex=False)

        # Save the modified DataFrame back to the CSV file
        recipes_data.to_csv(csv_file, index=False)
        print(f"Successfully replaced '&' with 'and' in the 'name' column of {csv_file}.")
    else:
        print("'name' column not found in the CSV file.")

# Specify your CSV file name
csv_file = "7k-dataset.csv"

# Call the function
replace_ampersand_in_names(csv_file)

