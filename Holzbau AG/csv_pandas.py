import pandas as pd
import os

def read_csv_to_dataframe(filename):
    try:
        dataframe = pd.read_csv(filename)
        return dataframe
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return None

def write_dataframe_to_csv(dataframe, filename):
    try:
        dataframe.to_csv(filename, index=False)
        print(f"Data written to {filename}")
    except Exception as e:
        print(f"Error writing data to {filename}: {e}")

# Example usage:
# data = read_csv_to_dataframe('your_csv_file.csv')
# Modify data as needed using pandas operations
# write_dataframe_to_csv(data, 'your_csv_file_updated.csv')