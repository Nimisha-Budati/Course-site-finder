# api/udemy.py

import requests

def get_udemy_courses(query):
    url = "https://www.udemy.com/api-2.0/courses/"

    params = {
        "search": query,
        "page_size": 5
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json, text/plain, */*"
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        return []

    data = response.json()

    courses = []

    for item in data.get("results", []):
        courses.append({
            "name": item.get("title"),
            "course_url": "https://www.udemy.com" + item.get("url"),
            "price": item.get("price", "N/A"),
            "rating": item.get("rating", 0)
        })

    return courses