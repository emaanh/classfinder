from courseScraper import getCourseHTML
from htmlScraper import parse_course_html, save_to_json
from codes import codes
import random
import time

output_json = "courses.json"
all_parsed_courses = []

print(f"Length of codes: {len(codes)}")
print(f"Estimated time: {2*len(codes)/60} mintues")

for code in codes:
    print(f"Processing course: {code}")
    html = getCourseHTML(code)
    parsed_courses = parse_course_html(html)
    all_parsed_courses.extend(parsed_courses)
    s = random.randint(1,3)
    print(f"Sleeping for {s} seconds" )
    time.sleep(random.randint(1,3))

save_to_json(all_parsed_courses, output_json)
print(f"Saved parsed courses to {output_json}")