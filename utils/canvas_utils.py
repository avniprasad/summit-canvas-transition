from canvasapi import Canvas
from bs4 import BeautifulSoup
import csv
from datetime import datetime
from urllib.parse import urlparse

def edit_page_body(page, updated_body):
  print("Updating Page: " + page.html_url)
  add_edited_pages_to_tracking_csv(page.html_url)
  return page.edit(wiki_page={'body': updated_body})

def edit_assignment_body(assignment, updated_body):
  print("Updating Assignment - " + assignment.html_url)
  add_edited_pages_to_tracking_csv(assignment.html_url)
  return assignment.edit(assignment={'description': updated_body})

def get_all_base_course_ids():
  return [x for x in range(631, 676)] + [x for x in range(677, 703)]  + [x for x in range(722, 728)]

def get_all_custom_course_ids():
  return [x for x in range(3537, 4369)] + [x for x in range(4538, 4559)]

def get_oer_course_ids():
  return [x for x in range(772, 778)] + [237,264, 265, 185, 266, 267]

def get_all_pages_for_course(course):
  all_pages = course.get_pages()
  return enumerate(all_pages)

def get_all_assignments_for_course(course):
  all_pages = course.get_assignments()
  return enumerate(all_pages)

# def get_all_quizzes_for_course(course):
#   all_pages = course.get_pages()
#   return enumerate(all_pages)

def get_iterable_modules_for_course(course):
  return enumerate(course.get_modules())

def get_iterable_module_items_for_module(module):
  return enumerate(module.get_module_items())

def get_html_content(canvas_element):
  breakpoint()
  #  if canvas_element.type

def find_text_in_html(html_content, search_text):
    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Function to recursively extract text from the soup object, preserving the textual order
    def extract_text(element):
        if isinstance(element, str):
            return element
        else:
            return ''.join(extract_text(child) for child in element.children)

    # Extract all text from the HTML
    extracted_text = extract_text(soup)

    # Normalize spaces in extracted text to ensure consistent searching
    normalized_text = ' '.join(extracted_text.split())

    # Check if the search phrase is in the extracted text
    return search_text in normalized_text

def find_and_replace_text_in_string(html_content, search_text, replace_text):
  if search_text in html_content:
    return True, html_content.replace(search_text, replace_text)
  else:
    return False, html_content

def find_and_replace_for_canvas_html(html_content, search_text, replace_text):
  was_updated, updated_html = find_and_replace_text_in_string(html_content, search_text, replace_text)
  has_additional_cases = find_text_in_html(updated_html, search_text)
  return was_updated, has_additional_cases, updated_html

def find_and_replace_for_page(page, search_text, replace_text, tracker):
  was_updated, has_additional_cases, updated_html = find_and_replace_for_canvas_html(page.body, search_text, replace_text)
  if was_updated:
    tracker["edited"] += 1
    edit_page_body(page, updated_html)
  if has_additional_cases:
    tracker["edited"] += 1
    print("Complex Case found in: " + page.title)

def add_edited_pages_to_tracking_csv(url):
    # File name of the CSV
    file_name = 'edited_pages.csv'

    # Get the current date in the format YYYY-MM-DD
    current_date = datetime.now().strftime('%Y-%m-%d')

    # Open the file in append mode, creating it if it doesn't exist
    with open(file_name, 'a', newline='') as csvfile:
        # Create a CSV writer object
        csvwriter = csv.writer(csvfile)

        # Write the URL and the current date to the CSV
        csvwriter.writerow([url, current_date])

    print(f"{url} added to {file_name}")

def add_url_rows_to_tracking_csv(rows):
    # File name of the CSV
    file_name = 'csv_exports/all_urls.csv'

    # Open the file in append mode, creating it if it doesn't exist
    with open(file_name, 'a', newline='') as csvfile:
        # Create a CSV writer object
        csvwriter = csv.writer(csvfile)
        for row in rows:
          # Write the URL and the current date to the CSV
          csvwriter.writerow(row)

    print(f"URLs added to {file_name}")


def add_attribution_rows_to_tracking_csv(rows):
    # File name of the CSV
    file_name = 'csv_exports/attribution_by_page.csv'

    # Open the file in append mode, creating it if it doesn't exist
    with open(file_name, 'a', newline='') as csvfile:
        # Create a CSV writer object
        csvwriter = csv.writer(csvfile)
        for row in rows:
          # Write the URL and the current date to the CSV
          csvwriter.writerow(row)

    print(f"URLs added to {file_name}")



def extract_domain_and_path(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.lower()
    path = parsed_url.path
    return domain, path