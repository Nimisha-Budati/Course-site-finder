import os
import django
import sys
import csv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from api.models import Course, Platform


def clean_float(value):
    try:
        return float(value)
    except:
        return 0


def clean_bool(value):
    return str(value).strip().lower() in ["true", "1", "yes"]


def run():
    with open('courses.csv', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            try:
                platform = Platform.objects.get(name=row['platform'])

                rating = clean_float(row.get('rating'))
                price = clean_float(row.get('price'))

                is_course_free = clean_bool(row.get('is_course_free'))
                certificate_available = clean_bool(row.get('certificate_available'))

                Course.objects.get_or_create(
                    name=row['name'],
                    platform=platform,
                    course_url=row['course_url'],
                    defaults={
                        "skill_level": row.get('skill_level') or "beginner",
                        "learning_mode": row.get('learning_mode') or "video",
                        "language": row.get('language') or "english",
                        "duration": row.get('duration') or "",
                        "rating": rating,
                        "is_course_free": is_course_free,
                        "price": price,
                        "certificate_available": certificate_available,
                    }
                )

                print(f"Added: {row['name']}")

            except Platform.DoesNotExist:
                print(f"Platform not found: {row['platform']}")

            except Exception as e:
                print(f"Error in row {row['name']}: {e}")

    print("CSV data loaded successfully!")


if __name__ == "__main__":
    run()