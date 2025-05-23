#!/usr/bin/env python3
import json
import re
import os
from datetime import datetime
import copy
from collections import defaultdict
import argparse
import sys


# === CONFIGURATION ===
MIN_ROOMS_TO_DISPLAY = 3  # Change this value to filter buildings with fewer unique rooms
MIN_COURSES_TO_DISPLAY = 4

FIRST_COL_WIDTH = 34  # Max width for the first column
SECOND_COL_WIDTH = 30  # Max width for the second column
EQUAL_SIGN_LENGTH = (FIRST_COL_WIDTH+SECOND_COL_WIDTH)+25  # Length of the '=' separator
DAYS = ['M', 'T', 'W', 'Th', 'F', 'Sat']
ROOM_ENDINGS = ["B","LL","L", "G"]
EARLIEST_START = "9:00am"
UNNEEDED_WORDS = ["hall", "building", "for", "and", "of", "the"]


def extract_building_prefix(location, building_names):
    """Extracts the building prefix from a location, handling 'B' and 'LL' corrections."""
    match = re.match(r"^([A-Za-z]+)(\d+[A-Za-z]?)$", location)
    if match:
        prefix = match.group(1)
        
        for ending in ROOM_ENDINGS:
            if prefix.endswith(ending) and prefix[:-(len(ending))] in building_names:
                return prefix[:-(len(ending))]

        return prefix  
    return None


def truncate_name(name, max_length):
    """Truncates name by removing words from the middle until it fits max_length, replacing them with '...'."""
    if len(name) <= max_length:
        return name
    
    words = name.split()
    
    words = [word for word in words if word.lower() not in UNNEEDED_WORDS]
    
    ellipse = "..." 
                
    curr_len = len(" ".join(words))
    if curr_len <= max_length:
        return " ".join(words)
    
    ellipse = "..." 
    
    while words and curr_len > max_length:
        curr_len -= (len(words[-1])+1)
        del words[-1]

    if(curr_len +len(ellipse) > max_length):
        ellipse = ""
        
    return " ".join(words) + ellipse



def print_buildings_table(buildings_list):
    """Prints buildings in a two-column format with truncated names, sorted by unique room count."""
    if not buildings_list:
        print("\nNo buildings meet the display criteria.")
        return

    padding = 0  

    # Calculate max digits in unique room counts to align numbers
    max_room_digits = max(len(str(count)) for _, _, count, _ in buildings_list)
    bracket_width = max_room_digits + 3  

    # Distribute buildings column-wise instead of row-wise
    mid = (len(buildings_list) + 1) // 2  
    left_column = buildings_list[:mid]  
    right_column = buildings_list[mid:]  

    separator_length = EQUAL_SIGN_LENGTH

    print("\nPopular Buildings ([n] = Number of rooms): ")
    print("=" * separator_length)

    for i in range(len(left_column)):  
        left_entry = left_column[i]
        left_name = truncate_name(left_entry[1], FIRST_COL_WIDTH)

        left_count_str = f"[{left_entry[2]}]"

        left_text = f"{left_name:<{FIRST_COL_WIDTH}} ({left_entry[0]}) {left_count_str:<{bracket_width}}"

        right_text = ""
        if i < len(right_column):
            right_entry = right_column[i]
            right_name = truncate_name(right_entry[1], SECOND_COL_WIDTH)

            right_count_str = f"[{right_entry[2]}]"

            right_text = f"{right_name:<{SECOND_COL_WIDTH}} ({right_entry[0]}) {right_count_str:<{bracket_width}}"

        print(f"{left_text}  {right_text}")  # Reduced spacing between columns

    print("=" * separator_length)

def time_to_value(time):
    """Converts a time string (e.g., '12:00 PM') to a numerical value."""
    try:
        time = time.strip().lower()
        day = "pm" in time
        time = time.replace("am", "").replace("pm", "").strip()
        if ":" not in time:
            time += ":00"
        hour, minute = map(int, time.split(":"))
        if hour < 1 or hour > 12 or minute < 0 or minute >= 60:
            return None  # Invalid time
        hour = hour % 12 + (12 * day)
        return (hour * 60 + minute) // 10  # Convert to value (divide by 10)
    except ValueError:
        return None

def value_to_time(value):
    """Converts a numerical value back to a time string."""
    value *= 10  # Convert back to minutes
    hour = value // 60
    minute = value % 60
    period = "PM" if hour >= 12 else "AM"
    hour = hour % 12 or 12  # Ensure 12-hour format

    time_str = f"{hour}:{minute:02} {period}"
    return "Midnight" if time_str == "11:50 PM" else time_str  # Convert 11:50 PM to Midnight

def split_days(schedule):
    """Extracts valid days from a schedule string."""
    return list(dict.fromkeys(re.findall(r'Th|M|T|W|F|Sat', schedule)))  # Remove duplicates

def find_negative_sequences(arr, min_length=2, earliest=EARLIEST_START):
    """Finds contiguous free time slots (-1s) within the specified time range."""
    earliest_val = time_to_value(earliest)
    sequences = []
    start = None

    for i, num in enumerate(arr):
        if i < earliest_val:
            continue
        if num == -1:
            if start is None:
                start = i
        else:
            if start is not None and i - start >= min_length:
                sequences.append((start, i))
            start = None
    if start is not None and len(arr) - start >= min_length:
        sequences.append((start, len(arr) - 1))

    return sequences

def free_times(rooms, room_prefix, day, specific_time=None):
    """Displays free times for rooms that match the prefix in the new format."""
    matched_rooms = sorted([r for r in rooms.keys() if r.startswith(room_prefix.upper())])
    
    if not matched_rooms:
        print(f"No rooms found matching '{room_prefix}'.")
        return

    for room in matched_rooms:
        if day not in rooms[room]:
            continue
        
        free_slots = find_negative_sequences(rooms[room][day])
        
        if specific_time is not None:
            # Find the first free slot that includes the specific time
            for start, end in free_slots:
                if start <= specific_time < end:
                    print(f"{room} available until {value_to_time(end)}")
                    break
        else:
            # Show all free slots for today
            if(free_slots):
                print(f"\n{room} available:")
                for start, end in free_slots:
                    print(f"{value_to_time(start)} to {value_to_time(end)}")

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_current_time_value():
    """Gets the current time in 10-minute slot format."""
    now = datetime.now()
    hour = now.hour % 12 or 12  # Convert to 12-hour format
    minute = now.minute
    period = "PM" if now.hour >= 12 else "AM"
    time_str = f"{hour}:{minute:02} {period}"
    return time_to_value(time_str)

def get_valid_day():
    """Prompts the user for a valid day input."""
    while True:
        day = input("> ")
        cleaned_day = clean_day(day)
        if cleaned_day:
            return cleaned_day
        print("Invalid day! Please enter M, T, W, Th, F, or Sat.")

def get_valid_time():
    """Prompts the user for a valid time input."""
    while True:
        time_str = input("> ").strip()
        time_val = time_to_value(time_str)
        if time_val is not None:
            return time_val
        print("Invalid time format! Please enter a valid time (e.g., 2:30pm).")

def process_raw_data():

    # Load course data
    try:
        with open('courses.json', 'r') as file:
            raw_courses = json.load(file)
    except FileNotFoundError:
        print("Error: courses.json file not found!")
        exit(1)

    # Load building names data (NEW JSON FORMAT: {"name": ..., "code": ...})
    try:
        with open('buildings.json', 'r') as file:
            raw_building_data = json.load(file)
    except FileNotFoundError:
        print("Error: buildings.json file not found!")
        exit(1)

    # Convert JSON into a dictionary mapping {CODE: NAME}
    building_names = {entry["code"]: entry["name"] for entry in raw_building_data}

    # Count how many **unique rooms** exist in each building
    building_room_counts = defaultdict(set)
    building_course_counts = defaultdict(set)

    # KAMB21/23
    # SCA214 SCAB105 SCESTG1 


    courses = []
    rooms = {}
    buildings = set()


    # Process course data to count how many **unique rooms** exist in each building
    for course in raw_courses:
        loc_matches = re.finditer(r"([A-Za-z]+)(\d+[A-Za-z]?)", course["location"])
        
        for loc_match in loc_matches:
            location = loc_match.group(0)
            
            time_pattern = r"(\d{2}:\d{2}(?:am|pm))-(\d{2}:\d{2}(?:am|pm))"
            time_matches = list(re.finditer(time_pattern, course["time"]))
            if time_matches:
                course["location"] = location
                building_prefix = extract_building_prefix(location, building_names)
                if building_prefix and building_prefix in building_names:
                    building_room_counts[building_prefix].add(location) 
                    building_course_counts[building_prefix] = building_course_counts.get(building_prefix, 0) + 1
                
                    
                    buildings.add(building_prefix.upper())
                for time_match in time_matches:
                    start_time = time_match.group(1)
                    end_time = time_match.group(2)

                    if not start_time or not end_time:
                        print("FAILED: ", course["time"])
                        quit()
                        
                    course_copy = copy.deepcopy(course)
                    course_copy["location"] = location
                    course_copy["start_time"] = start_time
                    course_copy["end_time"] = end_time            
                    course_copy["days"] = split_days(course_copy["days"])
                    
                    courses.append(course_copy)

    for course_id, course in enumerate(courses):
        room = course["location"].upper()  # Ensure case insensitivity
        if room not in rooms:
            rooms[room] = {}

        start = time_to_value(course["start_time"])
        end = time_to_value(course["end_time"])
        
        if start is None or end is None:
            print("FAILED2: ",course["start_time"], course["end_time"])
            quit()

        for day in DAYS:
            if day not in rooms[room]:
                rooms[room][day] = [-1] * 144  # 10-min slots from 8:00 AM to Midnight
            if day in course["days"]:
                for i in range(start, end):
                    rooms[room][day][i] = course_id
                    
    
    # Convert set counts to actual integer counts
    building_room_counts = {code: len(rooms) for code, rooms in building_room_counts.items()}

    # Keep only buildings that actually have classes and meet the minimum room requirement
    filtered_buildings = [
        (code, building_names[code], count, building_course_counts[code])
        for code, count in building_room_counts.items()
        if count >= MIN_ROOMS_TO_DISPLAY and building_course_counts[code] >= MIN_COURSES_TO_DISPLAY
    ]

    # Sort by number of **unique rooms** (descending)
    sorted_buildings = sorted(filtered_buildings, key=lambda x: x[3], reverse=True)
                    
    return rooms, sorted_buildings

def clean_day(day):
    match = re.match(r'TH|M|T|W|F|SAT|SAT', day.strip().upper())
    if not match:
        return None
    
    return match.group(0).capitalize()

def get_current_day():
    day = datetime.now().strftime("%a")
    return clean_day(day)

def main_loop():
    """Main CLI loop."""
    rooms, sorted_buildings = process_raw_data()
    while True:
        clear_screen()
        print("========= Empty Classroom Finder =========")
        print_buildings_table(sorted_buildings)

        room_prefix = input("Enter a room or building name (or leave blank to see all): ").strip().upper()
        if room_prefix and not any(r.startswith(room_prefix) for r in rooms.keys()):
            print(f"Error: No rooms or buildings found matching '{room_prefix}'.")
            input("\nPress Enter to try again...")
            continue

        print("\nWhen do you need the room?")
        print("1. Right now")
        print("2. At a specific time")
        print("3. See full availability for today")
        choice = input("> ").strip()
        

        if choice == "1":
            current_time_value = get_current_time_value()
            current_day = datetime.now().strftime("%a")[0]  # Get the current day as M/T/W/Th/F/Sat
            print(f"\nChecking rooms available at {value_to_time(current_time_value)} today ({current_day})...\n")
            free_times(rooms, room_prefix, current_day, current_time_value)

        elif choice == "2":
            print("\nEnter time (e.g., 2:00 PM):")
            time_val = get_valid_time()
            print("\nEnter the day you need the room for (M, T, W, Th, F, or Sat):")
            day = get_valid_day()
            print(f"\nChecking rooms available at {value_to_time(time_val)} on {day}...\n")
            free_times(rooms, room_prefix, day, time_val)
            

        elif choice == "3":
            day = get_current_day()  # Get the current day abbreviation (M, T, W, etc.)
            if(not day):
                print("FAILED DAY")
            else:
                print(f"\nShowing full availability for {room_prefix or 'all rooms'} on {day}...\n")
                free_times(rooms, room_prefix, day)

        input("\nPress Enter to search again or Ctrl+C to exit...")

def parse_time_string(time_str):
    if time_to_value(time_str) == None:
        raise ValueError(f"Invalid time format: {time_str}")

def parse_args():
    parser = argparse.ArgumentParser(description="ECF - Empty Classroom Finder")

    parser.add_argument("query", nargs="?", default=None,
                        help="Building, floor, or full room name (e.g., THT, THT1, THT123)")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("--at", metavar="TIME", type=str,
                       help="Specific time to check (e.g., 3pm, 14:00, 2:30pm, now)")
    group.add_argument("--full", action="store_true",
                       help="Show full-day availability")

    parser.add_argument("--day", type=str.lower, choices=DAYS,
                        help="Day of the week (e.g., mon, tue, wed)")

    return parser.parse_args()

def main():
    raw_args = sys.argv[1:]
    if not raw_args:
        main_loop()
        return
    
    args = parse_args()
    
    day = args.day or datetime.now().strftime("%a").lower()[:3]

    # Determine the mode
    if args.full:
        mode = "full"
        time = None
    elif args.at:
        try:
            time = parse_time_string(args.at)
            mode = "time"
        except ValueError as e:
            print(f"❌ {e}")
            sys.exit(1)
    else:
        mode = "time"
        time = datetime.now().time()

    # Output summary
    print("\n📋 Parsed Request:")
    print(f"  Location Filter : {args.query or 'ALL'}")
    print(f"  Mode            : {'Full-Day View' if mode == 'full' else 'Check Specific Time'}")
    print(f"  Day             : {day.capitalize()}")
    if time:
        print(f"  Time            : {time.strftime('%I:%M %p')}")
    print()
    

if __name__ == "__main__":
    main()