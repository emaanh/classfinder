import json

import re

def time_to_value(time):
    """Converts a time string (e.g., '12:00pm') to a numerical value."""
    day = (time[-2] == "p")  # Check if it's PM
    hour, minute = time[:-2].split(":")  # Split hour and minute
    hour = int(hour) % 12 + (12 * day)  # Convert to 24-hour format
    minute = int(minute)
    
    return (hour * 60 + minute) // 10  # Convert to value (divide by 10)

def value_to_time(value):
    """Converts a numerical value back to a time string."""
    value *= 10  # Convert back to minutes
    hour = value // 60  # Extract hour
    minute = value % 60  # Extract minutes

    day = "pm" if hour >= 12 else "am"  # Determine AM/PM
    hour = hour % 12  # Convert to 12-hour format
    if hour == 0:
        hour = 12  # Ensure 12-hour format

    return f"{hour}:{minute:02}{day}"  # Format properly



def has_number(s):
    return bool(re.search(r'\d', s))

def split_days(schedule: str):
    import re
    # Split on spaces and use regex to capture valid days
    days = re.findall(r'Th|M|T|W|F|Sat', schedule)
    # Remove duplicates while preserving order
    unique_days = list(dict.fromkeys(days))
    return unique_days

with open('courses.json', 'r') as file:
    raw_courses = json.load(file)

n = len(raw_courses)
courses = []

min_start = 1000000
max_end = 0

count = 0
for course in raw_courses:
    if(has_number(course["location"]) and len(course["time"].split("-")) == 2):
        time = course["time"]
        course.pop("time")
        if("-" in time):
            print(time)
        time_arr = time.split("-")
        if(len(time_arr) ==  1):
            print(course)
            
        start, end = time_arr
        course["start_time"] = start
        course["end_time"] = end
        course["days"] = split_days(course["days"])
        courses.append(course)


rooms = {}
days = ['Th','M','T','W','F','Sat']
    
    
for course_id in range(len(courses)):
    course = courses[course_id]        
    
    room = course["location"]

    if room not in rooms:
        rooms[room] = {}
        
    start = time_to_value(course["start_time"])
    end = time_to_value(course["end_time"])

    for day in days:
        if day not in rooms[room]:
            rooms[room][day] = [-1]*144 
        if day in course["days"]:
            for i in range(start, end):
                rooms[room][day][i] = course_id
                
    
            
            
def find_negative_sequences(arr, threshold=0, earliest="9:00am", latest="10:00pm"):
    """
    Finds contiguous sequences of -1 in the list and returns their start and end indices.
    
    :param arr: List of integers
    :param threshold: Minimum number of -1s required for a sequence to be included (default 0)
    :return: List of tuples (start_index, end_index)
    """
    earliest_val = time_to_value(earliest)
    latest_val = time_to_value(latest)
    
    sequences = []
    start = None  # To track the start of a sequence

    for i, num in enumerate(arr):
        if(i < earliest_val):
            continue
        if(i > latest_val):
            continue
        
        if num == -1:
            if start is None:  # Start a new sequence
                start = i
        else:
            if start is not None:  # End the sequence
                if i - start >= threshold:  # Check against threshold
                    sequences.append((start, i))
                start = None  # Reset start

    # Handle case where last sequence reaches the end of the list
    if start is not None and len(arr) - start >= threshold:
        sequences.append((start, len(arr) - 1))

    return sequences

def free_times(room, day):
    
    for r in rooms.keys():
        if r.startswith(room):
            list_tuples = find_negative_sequences(rooms[r][day], 2)
            
            print(f"\nAvailability in {r}:")
            
            for pair in list_tuples:
                start, end = pair
                start_str = value_to_time(start)
                end_str = value_to_time(end)
                
                if end_str == "11:50pm":
                    end_str = "Midnight"
                
                print(f"{start_str} to {end_str}")
                


room = input("What Room or Building?: ")
day = input("What day? ('M|T|W|Th|F|Sat'): ")
free_times(room, day)


#1 read json
#2 split times, split days
#3 dict[ID, dict[str,str]]
#4 array: room, day, times, ID
#5 for each room on a day. go through each course 


# dict[str (room), dict[str (day), list[ints (ID)]]]

