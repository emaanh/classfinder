import requests
import json
import re

# File paths
TXT_FILE = "buildings.txt"
JSON_FILE = "buildings.json"
API_URL = "https://api.concept3d.com/categories/53722?map=1928&children&key=0001085cc708b9cef47080f064612ca5"

def extract_building_code(name):
    """
    Extracts the building code from a name field (inside parentheses).
    Ensures the code is uppercase letters only (no numbers).
    """
    matches = re.findall(r"\(([A-Z]+)\)", name)  # Extract all uppercase codes inside parentheses
    return matches[-1] if matches else None  # Use the last valid uppercase code

def clean_building_name(name):
    """
    Cleans the building name by:
    - Removing any trailing text in parentheses that contains a code
    - Keeping only the actual name
    """
    code = extract_building_code(name)
    if code:
        # Remove the last parenthetical phrase if it contains the code
        name = re.sub(r"\s*\(" + code + r"\)$", "", name).strip()
    return name

def scrape_buildings_from_api():
    """Fetches buildings from the API and extracts name & code."""
    response = requests.get(API_URL)
    data = response.json()

    buildings = {}
    if "children" in data and "locations" in data["children"]:
        for item in data["children"]["locations"]:
            if "name" in item:
                name = item["name"].strip()
                code = extract_building_code(name)
                if code:
                    cleaned_name = clean_building_name(name)
                    # Keep the shortest name for the same code
                    if code not in buildings or len(cleaned_name) < len(buildings[code]):
                        buildings[code] = cleaned_name

    return buildings

def clean_txt_name(line):
    """
    Cleans the building name by removing:
    - Leading numbers and tabs/spaces
    - Any trailing spaces
    - Any text in parentheses (except the code)
    """
    # Remove the leading number + tab/space
    cleaned_line = re.sub(r"^\d+\s+", "", line).strip()

    # Extract code
    code = extract_building_code(cleaned_line)
    if not code:
        return None, None  # No valid code found

    # Remove everything in parentheses **except the last valid uppercase code**
    cleaned_name = clean_building_name(cleaned_line)

    return cleaned_name, code

def load_buildings_from_txt(file_path):
    """Reads building names and codes from a TXT file, keeping the shortest name per code."""
    buildings = {}
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                name, code = clean_txt_name(line)
                if code:
                    # Keep the shortest name if multiple exist for the same code
                    if code not in buildings or len(name) < len(buildings[code]):
                        buildings[code] = name
    except FileNotFoundError:
        print(f"Error: {file_path} not found!")
        exit(1)

    return buildings

def merge_and_update_json(api_buildings, txt_buildings, json_file):
    """
    Merges new buildings from API & TXT into JSON file.
    Keeps the shortest name when duplicates exist across sources.
    """
    combined_buildings = {}

    for code, name in {**api_buildings, **txt_buildings}.items():
        if code in api_buildings and code in txt_buildings:
            # If the code exists in both, take the shortest name
            combined_buildings[code] = min(api_buildings[code], txt_buildings[code], key=len)
        else:
            # Otherwise, take whatever is available
            combined_buildings[code] = name

    # Convert to JSON format
    updated_data = [{"name": name, "code": code} for code, name in sorted(combined_buildings.items())]

    # Write back to JSON
    with open(json_file, "w", encoding="utf-8") as file:
        json.dump(updated_data, file, indent=4)

    print(f"\n✅ Successfully updated {json_file} with {len(combined_buildings)} buildings.")


# Allow importing as a module or running standalone
if __name__ == "__main__":
    print("Fetching buildings from API...")
    api_buildings = scrape_buildings_from_api()

    print("Processing buildings from buildings.txt...")
    txt_buildings = load_buildings_from_txt(TXT_FILE)

    print("Merging data and updating JSON...")
    merge_and_update_json(api_buildings, txt_buildings, JSON_FILE)