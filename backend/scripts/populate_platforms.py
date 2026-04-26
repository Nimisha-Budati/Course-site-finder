import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from api.models import Platform


def run():
    platforms = [
        {"name": "Udemy", "website": "https://www.udemy.com"},
        {"name": "YouTube", "website": "https://www.youtube.com"},
        {"name": "NPTEL", "website": "https://onlinecourses.nptel.ac.in"},
        {"name": "Coursera", "website": "https://www.coursera.org"},
        {"name": "W3Schools", "website": "https://www.w3schools.com"},
        {"name": "Codechef", "website": "https://www.codechef.com"},
        {"name": "Hyperskill", "website": "https://hyperskill.org"},
        {"name": "edX", "website": "https://www.edx.org"},
        {"name": "Geeksforgeeks", "website": "https://www.geeksforgeeks.org"},
        {"name": "Codecademy", "website": "https://www.codecademy.com"},
        {"name": "Pluralsight", "website": "https://www.pluralsight.com"},
        {"name": "Sololearn", "website": "https://www.sololearn.com"},
        {"name": "Leetcode", "website": "https://leetcode.com"},
        {"name": "Freecodecamp", "website": "https://www.freecodecamp.org"}
    ]

    for p in platforms:
        Platform.objects.get_or_create(
            name=p["name"],
            defaults={"website": p["website"]}
        )

    print("All platforms added successfully!")


if __name__ == "__main__":
    run()