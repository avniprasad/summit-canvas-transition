import os
from dotenv import load_dotenv
from canvasapi import Canvas

# Get environment variables
load_dotenv()
API_URL = os.getenv('API_URL')
API_KEY = os.environ.get('API_KEY')

# Create Canvas instance
canvas = Canvas(API_URL, API_KEY)

# Get Course
course_id = 490 # example course using for testing code
course = canvas.get_course(course_id)
print(vars(course))


