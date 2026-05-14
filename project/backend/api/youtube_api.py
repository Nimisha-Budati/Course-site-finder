import requests
API_KEY = "AIzaSyDwNT_jaIy-ssWaTlOXQrAfEnv4Dv9n5Do"
def get_youtube_courses(query, language):
    query = query.lower().strip()
    if query == "c":
        search_query = "C programming"
    elif query == "c++":
        search_query = "C++ programming"
    else:
        search_query = query + " programming"
    if language == "hindi":
        search_query += " in Hindi"
    elif language == "telugu":
        search_query += " in Telugu"
    elif language == "english":
        search_query += " in English"
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": search_query,
        "key": API_KEY,
        "maxResults": 3,
        "type": "video"
    }
    response = requests.get(url, params=params)
    data = response.json()
    courses = []
    for item in data.get("items", []):
        title = item["snippet"]["title"]
        video_id = item["id"]["videoId"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        courses.append({
            "name": title,
            "platform": "YouTube",
            "course_url": video_url,
            "rating": None,
            "price": 0,
            "is_course_free": True,
            "certificate_available": False,
            "learning_mode": "video",
            "duration": "N/A"
        })
    filtered_courses = []
    for course in courses:
        title = course["name"].lower()
        if language == "hindi" and "hindi" not in title:
            continue
        if language == "telugu" and "telugu" not in title:
            continue
        if language == "english" and ("hindi" in title or "telugu" in title):
            continue
        filtered_courses.append(course)
    return filtered_courses