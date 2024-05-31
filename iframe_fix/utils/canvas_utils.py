import os
from canvasapi import Canvas
from dotenv import load_dotenv
from utils.csv_utils import add_edited_pages_to_tracking_csv

def get_canvas_instance():
    # Get environment variables
    load_dotenv()
    API_URL = os.getenv('API_URL')
    API_KEY = os.environ.get('API_KEY')

    # Create and return Canvas instance
    return Canvas(API_URL, API_KEY)

def get_html_content(course, page):
  full_page = course.get_page(page.page_id)
  return full_page.body

def edit_page_body(page, old_body, updated_body):
  print("Updating Page: " + page.html_url)
  add_edited_pages_to_tracking_csv(page.page_id, page.html_url, old_body, updated_body)
  return page.edit(wiki_page={'body': updated_body})