import requests
# ALI

def load_cookies_from_file(file_path):
    """
    Reads cookies from a text file and converts them into a dictionary.

    Args:
        file_path (str): Path to the cookies.txt file.

    Returns:
        dict: Dictionary where keys are cookie names and values are cookie values.
    """
    cookies = {}

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read().strip()  # Read and remove leading/trailing spaces

        # Split by '; ' since cookies are stored in key=value; key=value format
        cookie_pairs = content.split('; ')

        for pair in cookie_pairs:
            if '=' in pair:  # Ensure valid key=value pair
                key, value = pair.split('=', 1)  # Split only on first '='
                cookies[key] = value

    return cookies

def getCourseHTML(code):
    # URL for the courses page
    url = "https://webreg.usc.edu/Courses?Program="+code

    # Create a session
    session = requests.Session()

    # Define headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36",
        "Referer": "https://webreg.usc.edu/Departments",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9,fr;q=0.8",
        "Upgrade-Insecure-Requests": "1"
    }

    # Define cookies
    cookies = load_cookies_from_file("cookies.txt")

    # Fetch the page
    response = session.get(url, headers=headers, cookies=cookies)

    # Save the response content as an HTML file
    if response.status_code == 200:
        return response.text
        with open("webreg_courses.html", "w", encoding="utf-8") as file:
            file.write(response.text)
        print("Saved as webreg_courses.html")
    else:
        print(f"Failed to fetch page. Status code: {response.status_code}")
        return None