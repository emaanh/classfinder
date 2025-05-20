from courseScraper import getCourseHTML
from htmlScraper import parse_course_html, save_to_json
from scrape_building_names import scrape_buildings_from_api, load_buildings_from_txt, merge_and_update_json
from codes import codes
import random
import time

def scrape_courses():
    output_json = "courses.json"
    all_parsed_courses = []

    print(f"Length of codes: {len(codes)}")
    print(f"Estimated time: {2*len(codes)/60} mintues")

    for code in codes:
        print(f"Processing course: {code}")
        page_number = 1
        while(True):
            html = getCourseHTML(page_number, code)
            
            if html == None:
                break
            
            parsed_courses = parse_course_html(html)
            all_parsed_courses.extend(parsed_courses)
            page_number +=1
            s = random.randint(1,3)
            print(f"Sleeping for {s} seconds" )
            time.sleep(random.randint(1,3))

    save_to_json(all_parsed_courses, output_json)
    print(f"Saved parsed courses to {output_json}")

def scrape_buildings():
    TXT_FILE = "buildings.txt"
    JSON_FILE = "buildings.json"
    API_URL = "https://api.concept3d.com/categories/53722?map=1928&children&key=0001085cc708b9cef47080f064612ca5"

    print("Fetching buildings from API...")
    api_buildings = scrape_buildings_from_api()

    print("Processing buildings from buildings.txt...")
    txt_buildings = load_buildings_from_txt(TXT_FILE)

    print("Merging data and updating JSON...")
    merge_and_update_json(api_buildings, txt_buildings, JSON_FILE)

if __name__ == "__main__":
    # scrape_buildings()
    scrape_courses()
