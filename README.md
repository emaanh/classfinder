# **Campus Room Finder 📚**
A tool to quickly check for available rooms on campus. Find open rooms **right now**, at a specific time, or see full availability for a building/room. 

To gather it's data, this app scrapes a university’s course registration page, compiling all course schedules, including times and locations, to determine room availability.

---


## **Features**
✅ **Find available rooms** right now or at a specific time  
✅ **View full availability** for any building throughout the day  
✅ **Fast, robust, lightweight, and easy-to-use CLI**


## **Personal Motivation**
For some reason, I love hanging out in empty classrooms, using the blackboards, studying, talking to friends. Sometimes I want a private place to take a call or do homework between classes. 

---

## **Setup & Installation**
### **1. Clone the Repository**
```sh
git clone https://github.com/emaanh/roomfinder.git
cd campus-room-finder
```

### **2. Create a Virtual Environment & Install Dependencies**
```sh
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### **3. (Optional) New Semester or School Setup**
- **Default:** USC Spring 2025  
- To update for a different semester or school, **fill `cookies.txt` with your web registration cookies** and run:
  ```sh
  python setup.py
  ```

### **4. Run the App**
```sh
python app.py
```

---

## **Usage**
### **1. View Popular Buildings**
When you start the app, you will see a list of buildings with the number of available rooms:
```
Popular Buildings ([n] = Number of rooms):
====================================================
Dr. Joseph ... Public Affairs (DMC) [44]
Taper Hall (THH) [38]  
Kaprielian Hall (KAP) [34] 
Grace Ford Salvatori Hall (GFS) [31]  
...
=====================================================
Enter a room or building name (or leave blank to see all): 
```
- Enter a **room** (e.g. `THH101`) or a **building name** (e.g., `THH`, `DMC`) or **leave blank** to see all buildings.

---

### **2. Choose a Time**
After selecting a building, choose when you need a room:
```
When do you need the room?
1. Right now
2. At a specific time
3. See full availability for today
>
```
#### **Option 1: Find a Room "Right Now"**
- The app **automatically detects the current time and day**.
- **Example Output:**
  ```
  Checking rooms available at 2:00 PM on Wednesday...

  DMC157 available until 4:00 PM
  DMC102 available until 3:30 PM
  DMC204 available until Midnight
  DMC101 available until Midnight
  ```

#### **Option 2: Find a Room at a Specific Time**
- You will be asked to enter a **time** and **day**:
  ```
  Enter time (e.g., 2:00 PM): 2:00 PM
  Enter the day you need the room for: W
  ```

#### **Option 3: See Full Availability for Today**
- Shows all available time slots for a building throughout the day.
  ```
  Showing full availability for THH on F...

  THH117 available:
  9:00 AM to 10:00 AM
  10:50 AM to 12:00 PM
  1:50 PM to Midnight
  ```

---


## **Final Notes**
Sometimes clubs or staff reserve rooms and my program cannot account for that. If a room has an excessive amount of availability during a particular day, that room is more likely to be subject to reservations through your university.

Let me know if you need any changes!