import pandas as pd
import sys
import re

def clean_string(s):
    # Define a function to remove illegal characters
    if isinstance(s, str):
        return re.sub(r'[^\x20-\x7E]', '', s)  # Remove non-ASCII characters
    return s

def count_ips(input_file, output_file):
    # Load the CSV file
    df = pd.read_csv(input_file)
    
    # Check if the 'ip_client' column exists
    if 'ip_client' not in df.columns:
        print("Error: 'ip_client' column not found in the input CSV file.")
        return

    # Clean the data to remove illegal characters
    df = df.applymap(clean_string)

    # Count occurrences of each IP
    ip_counts = df['ip_client'].value_counts().reset_index()
    ip_counts.columns = ['ip_client', 'count']  # Rename columns for clarity

    # Merge counts back to original dataframe
    df_with_counts = pd.merge(df, ip_counts, on='ip_client', how='left')

    # Save the new dataframe to an Excel file
    df_with_counts.to_excel(output_file, index=False, engine='openpyxl')

    print(f"New Excel file created: {output_file}")

def main():
    # Check for command line arguments
    if len(sys.argv) < 3:
        print("Usage: python script.py <input_csv_file> <output_xlsx_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    count_ips(input_file, output_file)

if __name__ == "__main__":
    main()
