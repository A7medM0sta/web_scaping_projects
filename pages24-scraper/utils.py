import re
import csv

from urllib.parse import urlparse
def clean_phone_number(phone_number):
    cleaned_number = re.sub(r'\D', '', phone_number)
    if cleaned_number.startswith('1') and len(cleaned_number) == 11:
        cleaned_number = cleaned_number[1:]
    formatted_number = re.sub(
        r'(\d{3})(\d{3})(\d{4})', r'(\1) \2-\3', cleaned_number)
    return formatted_number

# =================================================================
#  Dict to CSV Function
# ==================================================================


def list_of_dicts_to_csv(data_list, csv_filename):
    """
    Convert a list of dictionaries to a CSV file with the specified filename.
    """
    if not data_list:
        print("Input list is empty.")
        return

    # Extract column headers from the keys of the first dictionary
    headers = list(data_list[0].keys())

    # Write data to CSV file
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)

        # Write header row
        writer.writeheader()

        # Write data rows
        writer.writerows(data_list)

    print(f"Data stored to '{csv_filename}' successfully.")