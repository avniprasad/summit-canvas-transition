import os
from dotenv import load_dotenv
from canvasapi import Canvas
from bs4 import BeautifulSoup

# Get environment variables
load_dotenv()
API_URL = os.getenv('API_URL')
API_KEY = os.environ.get('API_KEY')

# Create Canvas instance
canvas = Canvas(API_URL, API_KEY)

def get_html_content(course, page):
  full_page = course.get_page(page.page_id)
  return full_page.body

def get_iframes_elems(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.find_all('iframe')

def is_drive_link(src):
    return "drive.google.com" in src

def fix_iframes_for_course(course_id):
    course = canvas.get_course(course_id)
    # Q: do I need to get all the pages or can this be limited to type of course pages? 
    # ex. assignment pages
    all_pages = course.get_pages()
    fixed_pages = []
    counter = 0
    for page in all_pages:
        html_content = get_html_content(course, page)
        iframe_elems = get_iframes_elems(html_content)
        has_drive_iframe = False
        for iframe in iframe_elems:
            counter += 1
            src = iframe['src']
            if is_drive_link(src):
                has_drive_iframe = True
        
        if has_drive_iframe:
            # TODO replace iframe 
            fixed_pages.append(page.page_id)
        
        if counter > 10:
            break
    return fixed_pages


course_id = 490 # example course using for testing code
fixed_iframes = fix_iframes_for_course(course_id)
print(fixed_iframes)


