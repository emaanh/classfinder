import json
from bs4 import BeautifulSoup
import re

def clean_text(text):
    """Removes extra spaces, newlines, and leading/trailing characters."""
    return ' '.join(text.strip().split())

def remove_prefix(text):
    """Removes common prefixes like 'Time:', 'Location:', etc., if they appear at the start of the string."""
    return re.sub(r'^(Time|Location|Instructor|Days|Registered|Units|Type):\s*', '', text, flags=re.IGNORECASE)


def parse_course_html(html):
    soup = BeautifulSoup(html, 'html.parser')

    sections_list = []
    
    # Find all course headers
    course_headers = soup.find_all("div", class_="course-header")
    
    for course_header in course_headers:
        course_title_elem = course_header.find("a", class_="course-title-indent")
        if course_title_elem:
            course_id = clean_text(course_title_elem.find("span", class_="crsID").text.replace(":", ""))
            course_name = clean_text(course_title_elem.find("span", class_="crsTitl").text)

            # Get course description
            course_details_div = course_header.find_next_sibling("div", class_="accordion-content-area")
            course_description = ""
            if course_details_div:
                description_elem = course_details_div.find("div", class_="bs-callout")
                if description_elem:
                    course_description = clean_text(description_elem.text)

            # Find all sections related to this course
            section_rows = course_details_div.find_all("div", class_="section-row") if course_details_div else []
            
            for section in section_rows:
                section_data = {
                    "course_id": course_id,
                    "course_name": course_name,
                    "description": course_description,
                    "section": clean_text(section.find("b").text) if section.find("b") else "",
                    "type": remove_prefix(clean_text(section.find("span", class_="course-section-lecture").text)) if section.find("span", class_="course-section-lecture") else "",
                    "units": remove_prefix(clean_text(section.find_all("span", class_="section_row")[3].text)) if len(section.find_all("span", class_="section_row")) > 3 else "",
                    "registered": remove_prefix(clean_text(section.find_all("span", class_="section_row")[4].text)) if len(section.find_all("span", class_="section_row")) > 4 else "",
                    "time": remove_prefix(clean_text(section.find_all("span", class_="section_row")[5].text)) if len(section.find_all("span", class_="section_row")) > 5 else "",
                    "days": remove_prefix(clean_text(section.find_all("span", class_="section_row")[6].text)) if len(section.find_all("span", class_="section_row")) > 6 else "",
                    "instructor": remove_prefix(clean_text(section.find_all("span", class_="section_row")[7].text)) if len(section.find_all("span", class_="section_row")) > 7 else "",
                    "location": remove_prefix(clean_text(section.find_all("span", class_="section_row")[8].text)) if len(section.find_all("span", class_="section_row")) > 8 else ""
                }

                sections_list.append(section_data)

    return sections_list

def save_to_json(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
