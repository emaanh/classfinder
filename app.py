import json
import re
import os
from datetime import datetime
import copy

def time_to_value(time):
    """Converts a time string (e.g., '12:00 PM') to a numerical value."""
    try:
        time = time.strip().lower()
        day = "pm" in time
        time = time.replace("am", "").replace("pm", "").strip()
        hour, minute = map(int, time.split(":"))
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

def extract_building_prefix(location):
    """Extracts the building prefix from a location (e.g., 'THH' from 'THH117')."""
    match = re.match(r"^[A-Za-z]+", location)
    return match.group(0) if match else None

# Load course data
try:
    with open('courses.json', 'r') as file:
        raw_courses = json.load(file)
except FileNotFoundError:
    print("Error: courses.json file not found!")
    exit(1)

# Process course data
courses = []
rooms = {}
days = ['M', 'T', 'W', 'Th', 'F', 'Sat']
buildings = set()

for course in raw_courses:
    if re.search(r'\d', course["location"]) and "-" in course["time"]:
        times = course["time"].split(" ")
        for time in times:
            course2 = copy.deepcopy(course)
            time_arr = time.split("-")
            if(len(time_arr) !=2):
                print(times)
                continue
            

            course2["start_time"], course2["end_time"] = time_arr
            course2["days"] = split_days(course2["days"])
            courses.append(course2)

        # Extract building prefix and store it
        building_prefix = extract_building_prefix(course["location"])
        if building_prefix:
            buildings.add(building_prefix.upper())

for course_id, course in enumerate(courses):
    room = course["location"].upper()  # Ensure case insensitivity
    if room not in rooms:
        rooms[room] = {}

    start = time_to_value(course["start_time"])
    end = time_to_value(course["end_time"])
    if start is None or end is None:
        continue

    for day in days:
        if day not in rooms[room]:
            rooms[room][day] = [-1] * 144  # 10-min slots from 8:00 AM to Midnight
        if day in course["days"]:
            for i in range(start, end):
                rooms[room][day][i] = course_id

def find_negative_sequences(arr, min_length=2, earliest="9:00 AM", latest="10:00 PM"):
    """Finds contiguous free time slots (-1s) within the specified time range."""
    earliest_val = time_to_value(earliest)
    latest_val = time_to_value(latest)
    sequences = []
    start = None

    for i, num in enumerate(arr):
        if i < earliest_val or i > latest_val:
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

def free_times(room_prefix, day, specific_time=None):
    """Displays free times for rooms that match the prefix in the new format."""
    matched_rooms = [r for r in rooms.keys() if r.startswith(room_prefix.upper())]
    
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
            for start, end in free_slots:
                print(f"{room} available until {value_to_time(end)}")

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

def main():
    """Main CLI loop."""
    while True:
        clear_screen()
        print("==== Campus Room Finder ====\n")

        print("1. Find a room")
        print("2. List all buildings")
        choice = input("> ").strip()

        if choice == "2":
            print("\nAvailable buildings:")
            print(", ".join(sorted(buildings)))
            input("\nPress Enter to continue...")
            continue

        # If user chooses to find a room
        room_prefix = input("Enter a room or building name (or leave blank to see all): ").strip().upper()
        if not room_prefix:
            room_prefix = ""  # Show all rooms

        print("\nWhen do you need the room?")
        print("1. Right now")
        print("2. At a specific time")
        print("3. See full availability for today")
        choice = input("> ").strip()

        if choice == "1":
            current_time_value = get_current_time_value()
            current_day = datetime.now().strftime("%a")[0]  # Get the current day as M/T/W/Th/F/Sat
            print(f"\nChecking rooms available at {value_to_time(current_time_value)} today ({current_day})...\n")
            free_times(room_prefix, current_day, specific_time=current_time_value)

        elif choice == "2":
            specific_time = input("\nEnter time (e.g., 2:00 PM): ").strip()
            time_val = time_to_value(specific_time)
            if time_val is None:
                print("Invalid time format!")
                input("Press Enter to continue...")
                continue

            print("\nEnter the day you need the room for (e.g., M, T, W, Th, F, Sat):")
            day = input("> ").strip().capitalize()
            if day not in days:
                print("Invalid day! Please enter M, T, W, Th, F, or Sat.")
                input("Press Enter to continue...")
                continue

            print(f"\nChecking rooms available at {specific_time} on {day}...\n")
            free_times(room_prefix, day, specific_time=time_val)

        elif choice == "3":
            print(f"\nShowing full availability for {room_prefix or 'all rooms'}...\n")
            day = datetime.now().strftime("%a")[0]
            free_times(room_prefix, day)

        input("\nPress Enter to search again or Ctrl+C to exit...")

if __name__ == "__main__":
    main()