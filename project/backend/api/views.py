from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q,Avg
from .models import Course, Review
from .models import Course, Favorite, Review, SearchHistory, UserPreference
from .udemy_scraper import get_udemy_data
from .youtube_api import get_youtube_courses
from .models import SearchHistory
from .udemy import get_udemy_courses
import re

def auth_view(request):
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "login":
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("dashboard")
            else:
                messages.error(request, "Invalid username or password")
                return redirect("auth")
        elif action == "register":
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")
            if password != confirm_password:
                messages.error(request, "Passwords do not match")
                return redirect("auth")
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
                return redirect("auth")
            if len(password) < 4:
                messages.error(request, "Password must be at least 4 characters")
                return redirect("auth")
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            #login(request, user)
            #messages.success(request, "Account created successfully")
            #return redirect("auth")
            messages.success(request, "Account created successfully. Please login.")
            return redirect("/auth/?mode=login")
    return render(request, "auth.html")
def logout_view(request):
    logout(request)
    return redirect("auth")

@login_required
def home_view(request):
    return render(request, "home.html")

@login_required
def dashboard(request):
    favorites_count = Favorite.objects.filter(user=request.user).count()
    reviews_count = Review.objects.filter(user=request.user).count()
    return render(request, "dashboard.html", {
        "favorites_count": favorites_count,
        "reviews_count": reviews_count
    })

def about_view(request):
    return render(request, "about.html")

def selection_view(request):
    if request.method == "POST":
        course_name = request.POST.get("course", "").strip()
        skill_level = request.POST.get("skillLevel", "").lower().strip()
        plan = request.POST.get("plan", "").lower().strip()
        certificate = request.POST.get("certificate", "").lower().strip()
        learning_mode = request.POST.get("learningMode", "").lower().strip()
        language = request.POST.get("language", "").lower().strip()
        platform = request.POST.get('platform') or "Unknown"
        UserPreference.objects.create(
            user=request.user,
            course_name=course_name,
            skill_level=skill_level,
            plan=plan,
            certification_needed=(certificate == "yes"),
            learning_mode=learning_mode,
            language=language,
        )
        if course_name:
            SearchHistory.objects.create(
                user=request.user,
                course_name=course_name,
                skill_level=skill_level,
                plan=plan,
                language=language,
                learning_mode=learning_mode,
                certification_needed=(certificate == "yes")
        )
        if course_name.lower() == "c":
            queryset = Course.objects.filter(name__iexact="c")
        elif course_name.lower() in ["c++", "cpp"]:
            queryset = Course.objects.filter(name__icontains="c++")
        else:
            queryset = Course.objects.filter(name__icontains=course_name)
        if skill_level:
            queryset = queryset.filter(skill_level__iexact=skill_level)
        if language:
            queryset = queryset.filter(language__iexact=language)
        if learning_mode:
            queryset = queryset.filter(learning_mode__iexact=learning_mode)
        if plan == "free":
            queryset = queryset.filter(is_course_free=True)
        elif plan == "paid":
            queryset = queryset.filter(is_course_free=False)

        if certificate == "yes":
            queryset = queryset.filter(certificate_available=True)
        elif certificate == "no":
            queryset = queryset.filter(certificate_available=False)
        if not queryset.exists():
            queryset = Course.objects.none()
        queryset = queryset.order_by(
            '-popularity_score',
            '-views_count'
        )
        top_courses = queryset[:5]
        final_courses = []
        for course in top_courses:
            final_courses.append({
                "id": course.id,
                "name": course.name,
                "platform": course.platform.name if course.platform else "-",
                "rating": course.rating if course.rating is not None else 0,
                "duration": course.duration or "N/A",
                "price": "Free" if course.is_course_free else f"₹{course.price}" if course.price else "N/A",
                "certificate": "Yes" if course.certificate_available else "No",
                "url": course.course_url,
                "reviews": []
            })
        youtube_courses = []
        allow_youtube = (plan == "free" or not final_courses) and certificate != "yes"
        if allow_youtube and learning_mode != "text":
            try:
                youtube_courses = get_youtube_courses(course_name, language) or []
            except:
                youtube_courses = []
        for yt in youtube_courses[:(5 - len(final_courses))]:
            final_courses.append({
                "id": None,
                "name": yt.get("name"),
                "platform": "YouTube",
                "rating": 0,
                "duration": yt.get("duration", "-"),
                "price": "Free",
                "certificate": False,
                "url": yt.get("course_url"),
                "reviews": []
            })
        return render(request, "results.html", {
            "courses": final_courses,
            "reviews": Review.objects.select_related('user', 'course').order_by('-created_at')
        })

    return render(request, "selection.html")
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from .models import Course, Review
from django.http import JsonResponse

@login_required
def add_review(request):
    if request.method == "POST":
    
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")
        course_id = request.POST.get("course_id")
        course_url = request.POST.get("course_url")
        course_name = request.POST.get("course_name")

        if not rating or not comment:
            return JsonResponse({"message": "Invalid data"}, status=400)

        course = None
        if course_id and course_id not in ["None", "", "youtube"]:
            try:
                course = Course.objects.get(id=int(course_id))
            except (Course.DoesNotExist, ValueError):
                course = None
        Review.objects.create(
            user=request.user,
            rating=int(rating),
            comment=comment,
            course=course,
            course_url=course_url if not course else course.course_url,
            course_name=course_name if not course else course.name
        )

        return JsonResponse({"message": "Review added successfully!"})

    return JsonResponse({"message": "Invalid request"}, status=400)
@login_required
def delete_review(request, review_id):
    if request.method == "POST":
        review = get_object_or_404(Review, id=review_id)
        if review.user != request.user:
            return JsonResponse({"message": "Not allowed"}, status=403)
        review.delete()
        return JsonResponse({"message": "Deleted successfully"})
    return JsonResponse({"message": "Invalid request"}, status=400)
from django.db.models import Avg

def result_view(request):
    query = request.GET.get('q', '').strip()
    courses = Course.objects.all()
    if query:
        courses = courses.filter(name__icontains=query)
    reviews = Review.objects.select_related('user', 'course').order_by('-created_at')
    return render(request, 'results.html', {
        'courses': courses,
        'reviews': reviews,
        'query': query
    })
@login_required
def history_view(request):
    history = SearchHistory.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "history.html", {
        "history": history
    })
@login_required
def delete_history(request, id):
    if request.method == "POST":
        item = get_object_or_404(SearchHistory, id=id, user=request.user)
        item.delete()
    return redirect('history')

@login_required
def mark_helpful(request):
    return redirect("results")
@login_required

def saved_view(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('course')

    return render(request, "saved.html", {
        "favorites": favorites
    })

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Favorite

import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Favorite

@csrf_exempt
@login_required
def save_course(request):
    if request.method == "POST":
        data = json.loads(request.body)
        course_id = data.get("course_id")
        name = data.get("course_name")
        url = data.get("course_url")
        if course_id in ["", "None", "youtube"]:
            course_id = None
        exists = Favorite.objects.filter(
            user=request.user,
            url=url
        ).exists()
        if exists:
            return JsonResponse({"message": "Already saved!"})
        Favorite.objects.create(
            user=request.user,
            course_id=course_id,
            title=name,
            url=url,
            platform="YouTube" if not course_id else "Course"
        )
        return JsonResponse({"message": "Saved successfully!"})
    return JsonResponse({"message": "Invalid request"}, status=400)
    
@login_required
def remove_favorite(request, id):
    fav = get_object_or_404(Favorite, id=id, user=request.user)
    fav.delete()
    return JsonResponse({"message": "Removed successfully"})

import json
@login_required
def save_youtube(request):
    if request.method == "POST":
        data = json.loads(request.body)
        title = data.get("title")
        url = data.get("url")
        print("YOUTUBE SAVE:", title, url) 
        fav, created = Favorite.objects.get_or_create(
            user=request.user,
            title=title,
            url=url
        )
        return JsonResponse({"created": created})