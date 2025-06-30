import csv
import os
import argparse

# Author: Daeho Chang
# Email: daeho.chang@anl.gov
# Created: June 30, 2025
# Description: Extracts a markdown-style table from a text file and saves it as a CSV file.

def extract_table_to_csv(input_file_path):
    """
    Extracts a markdown-style table from a text file and saves it as a CSV file.

    The script identifies the table based on a header containing 'code_of_account'.
    It assumes the table is formatted with '|' as column separators and '+--' as
    horizontal rule.

    Args:
        input_file_path (str): The path to the input .out file.
    """
    output_filename = "accel_2214_output_excel.csv"

    if not os.path.isfile(input_file_path):
        print(f"Error: Input file not found at '{input_file_path}'")
        return

    with open(input_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    header = []
    data_rows = []
    
    header_keyword = 'code_of_account'
    header_index = -1
    for i, line in enumerate(lines):
        if header_keyword in line and '|' in line:
            header_index = i
            break
            
    if header_index == -1:
        print(f"Error: Could not find table header with keyword '{header_keyword}'")
        return

    header_line = lines[header_index]
    header = [h.strip() for h in header_line.split('|') if h.strip()]
    
    # Table data starts 2 lines after the header (skipping the separator line)
    for i in range(header_index + 2, len(lines)):
        line = lines[i].strip()
        if line.startswith('+--'): # End of table
            break
        
        if '|' in line:
            row = [item.strip() for item in line.split('|') if item.strip()]
            # Ensure the row has the same number of columns as the header
            if len(row) == len(header):
                data_rows.append(row)

    if not data_rows:
        print("Warning: No data rows were found for the table.")
        return

    # Save output in the same directory as the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_filepath = os.path.join(script_dir, output_filename)

    try:
        with open(output_filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)
            writer.writerows(data_rows)
        print(f"Successfully created CSV file at: {os.path.abspath(output_filepath)}")
    except IOError as e:
        print(f"Error: Could not write to file '{output_filepath}'. Reason: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Extracts a table from a text file and saves it as a CSV file.',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        'input_file', 
        help='Path to the input file (e.g., output.out).'
    )
    
    args = parser.parse_args()
    
    extract_table_to_csv(args.input_file) 