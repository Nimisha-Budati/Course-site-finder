import requests
import re
import json

def get_udemy_data(url):

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        r = requests.get(url, headers=headers)
        html = r.text

        # 🔥 Udemy stores data inside JSON in script tag
        match = re.search(r'window\\.__INITIAL_DATA__\\s*=\\s*(\\{.*?\\});', html)

        if not match:
            return None, None

        data = json.loads(match.group(1))

        rating = None
        price = None

        # 🔍 safe extraction (structure may vary)
        try:
            rating = data["course"]["rating"]
        except:
            pass

        try:
            price = data["course"]["price"]
        except:
            pass

        return rating, price

    except Exception as e:
        print("Scraper error:", e)
        return None, None