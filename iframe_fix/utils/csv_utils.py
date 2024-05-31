import csv
import os
from datetime import datetime

def add_edited_pages_to_tracking_csv(page_id, url, old_content, new_content):
    # File name of the CSV
    file_name = 'edited_pages.csv'
    fields = ['Timestamp', 'Page Id', 'Url', 'Old Content', 'New Content']
    file_exists = os.path.isfile(file_name)

    # Open the file in append mode, creating it if it doesn't exist
    with open(file_name, 'a', newline='') as csvfile:
        # Create a CSV writer object
        csvwriter = csv.writer(csvfile)
        # Add headers if newly created file
        if not file_exists:
            csvwriter.writerow(fields)

        # Write the URL and the current date to the CSV
        csvwriter.writerow([datetime.now(), page_id, url, old_content, new_content])

    print(f"{url} added to {file_name}")