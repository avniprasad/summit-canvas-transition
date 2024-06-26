from bs4 import BeautifulSoup
from utils.canvas_utils import get_canvas_instance, get_html_content, edit_page_body

def is_drive_link(src):
    return "drive.google.com" in src

def create_link_replacement(soup, src):
    link_text = "Click here to access this resource"
    link_elem = soup.new_tag('a', href=src)
    link_elem.string = link_text
    return link_elem

def fix_iframes_for_course(course_id):
    canvas = get_canvas_instance()
    course = canvas.get_course(course_id)
    # Q: do I need to get all the pages or can this be limited to type of course pages? 
    # ex. assignment pages
    all_pages = course.get_pages()
    fixed_pages = []
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
            edit_page_body(page, html_content, str(soup))
            fixed_pages.append(page.page_id)
    return fixed_pages


course_id = 490 # example course using for testing code
fixed_iframes = fix_iframes_for_course(course_id)
print(fixed_iframes)