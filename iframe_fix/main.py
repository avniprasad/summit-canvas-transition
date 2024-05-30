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

def is_drive_link(src):
    return "drive.google.com" in src

def create_link_replacement(soup, src):
    link_text = "Click here to access this resource"
    link_elem = soup.new_tag('a', href=src)
    link_elem.string = link_text
    return link_elem

def fix_iframes_for_course(course_id):
    course = canvas.get_course(course_id)
    # Q: do I need to get all the pages or can this be limited to type of course pages? 
    # ex. assignment pages
    all_pages = course.get_pages()
    fixed_pages = []
    # counter = 0
    for page in all_pages:
        html_content = get_html_content(course, page)
        soup = BeautifulSoup(html_content, 'html.parser')
        iframe_elems = soup.find_all('iframe')

        has_drive_iframe = False
        for iframe in iframe_elems:
            src = iframe['src']
            if is_drive_link(src):
                has_drive_iframe = True
                link_elem = create_link_replacement(soup, src)
                iframe.replace_with(link_elem)
        
        if has_drive_iframe:
            # counter += 1
            # if counter > 10:
            #     break
            # TODO push html change to the Canvas page
            fixed_pages.append(page.page_id)
    return fixed_pages


course_id = 490 # example course using for testing code
fixed_iframes = fix_iframes_for_course(course_id)
# RESULT:
# [73717, 73722, 73753, 73767, 73768, 73777, 73778, 73779, 73780, 73781, 73782,
# 73792, 73804, 73809, 73811, 73813, 73825, 73826, 73827, 73828, 73829, 73836,
# 73841, 73858, 73871, 73872, 73874, 73876, 73878, 73879, 73880, 73881, 73888,
# 73892, 73893, 73894, 73895, 73896, 73897, 73898, 73899, 73901, 73902, 73903,
# 73904, 73905, 73906, 73907, 73908, 73909, 73910, 73911, 73912, 73917, 73920,
# 73923, 73925, 73935, 73943, 73951, 73968, 73969, 73975, 74002, 74010, 74011,
# 74012, 74013, 74014, 74049, 74055, 74056, 74057, 74058, 74061, 74064, 74077,
# 74078, 74088, 74089, 74094, 74097, 74099, 74101, 74316, 74317, 74318, 74319,
# 74321, 74322, 74323, 74324, 74325, 74326, 74327, 74328, 74330, 74331, 74332,
# 74333, 74334, 74336, 74337, 74338, 74342, 74343, 74348, 74351, 74353, 74357,
# 74358, 74361, 74362, 74363, 74366, 74372, 74373, 74374, 74375, 74376, 74388,
# 74396, 74397, 74399, 74411, 74412, 74413, 74414, 74416, 74417, 74418, 74419,
# 74420, 74422, 74423, 74425, 74426, 74427, 74428, 74429, 74431, 74432, 74433,
# 74434, 74435, 74436, 74443, 74445, 74446, 74448]
print(fixed_iframes)


