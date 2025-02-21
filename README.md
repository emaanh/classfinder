# **Campus Room Finder (CLI App)**
A simple **command-line tool** to check for available study rooms on campus. It allows students to quickly find empty rooms **right now**, at a specific time, or see the full availability of a room/building for the day.

---

## **Features**
✅ **Find available rooms** at the current time, a specific time, or see full availability for the day  
✅ **Lists all buildings** available on campus  
✅ **Automatically detects the current day & time** when searching "right now"  
✅ **Minimal and clean output** (only displays available rooms)  

---

## **Installation**
### **Prerequisites**
- Python 3.x installed on your system
- A valid `courses.json` file containing the course schedule

### **Clone the repository**
```sh
git clone https://github.com/yourusername/campus-room-finder.git
cd campus-room-finder
```

### **Run the app**
```sh
python find_room.py
```

---

## **Usage**
### **1. Select an option**
When you run the program, you will be given two choices:
```
==== Campus Room Finder ====

1. Find a room
2. List all buildings
> 
```
- **Option 1** → Find a study room  
- **Option 2** → List all buildings available on campus  

---

### **2. Searching for a Room**
After selecting **option 1**, enter a **room or building name** (e.g., "THH" or "ENG-204") or leave it blank to see all rooms.
```
Enter a room or building name (or leave blank to see all): THH
```

---

### **3. Choose a Time**
Next, you will be asked **when** you need the room:
```
When do you need the room?
1. Right now
2. At a specific time
3. See full availability for today
> 
```

- **Option 1 ("Right now")**  
  - The app will use the **current time & day automatically**  
  - **Example Output:**
    ```
    Checking rooms available at 3:20 PM today (T)...

    THH117 available until 4:00 PM
    THH105 available until 5:00 PM
    THH111 available until Midnight
    ```

- **Option 2 ("At a specific time")**  
  - You will be prompted to enter a time:
    ```
    Enter time (e.g., 2:00 PM): 
    ```
  - Then, you will enter the **day**:
    ```
    Enter the day you need the room for (e.g., M, T, W, Th, F, Sat):
    ```

- **Option 3 ("See full availability for today")**  
  - The app will **list all available times for the room/building for the entire day**  

---

## **Example Searches**
### **Find available rooms in THH right now**
```
$ python find_room.py
==== Campus Room Finder ====

1. Find a room
2. List all buildings
> 1

Enter a room or building name (or leave blank to see all): THH

When do you need the room?
1. Right now
2. At a specific time
3. See full availability for today
> 1

Checking rooms available at 3:20 PM today (T)...

THH117 available until 4:00 PM
THH105 available until 5:00 PM
THH111 available until Midnight
```

---

### **Find available rooms in KAP at 2:30 PM on Wednesday**
```
$ python find_room.py
==== Campus Room Finder ====

1. Find a room
2. List all buildings
> 1

Enter a room or building name (or leave blank to see all): KAP

When do you need the room?
1. Right now
2. At a specific time
3. See full availability for today
> 2

Enter time (e.g., 2:00 PM): 2:30 PM

Enter the day you need the room for (e.g., M, T, W, Th, F, Sat):
> W

Checking rooms available at 2:30 PM on W...

KAP104 available until 4:00 PM
KAP210 available until 6:30 PM
```

---

### **List all available buildings**
```
$ python find_room.py
==== Campus Room Finder ====

1. Find a room
2. List all buildings
> 2

Available buildings:
ACB, ENG, GFS, KAP, THH

Press Enter to continue...
```

---

## **JSON File Format (`courses.json`)**
The `courses.json` file should contain an array of course objects with **location, time, and days**.
```json
[
  {
    "location": "THH117",
    "time": "2:00 PM-3:30 PM",
    "days": "M W F"
  },
  {
    "location": "KAP104",
    "time": "10:00 AM-12:00 PM",
    "days": "T Th"
  }
]
```

---

## **Known Issues & Future Improvements**
- The app **does not yet handle multi-day searches** (e.g., "Find a room on both Tuesday and Thursday").  
- **Holiday schedules** are not considered; all courses are assumed to follow a normal week.  
- **Would you like any extra features?** Feel free to submit an issue.
