"""from django.db import models
from django.contrib.auth.models import User
class Platform(models.Model):
    name = models.CharField(max_length=200, unique=True)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name
class Course(models.Model):
    SKILL_LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced')
    ]
    LEARNING_MODE_CHOICES = [
        ('video', 'Video'),
        ('text', 'Text'),
        ('mixed', 'Mixed')
    ]
    LANGUAGE_CHOICES = [
        ('english', 'English'),
        ('hindi', 'Hindi')
    ]
    name = models.CharField(max_length=500)
    platform = models.ForeignKey(
        'Platform',
        on_delete=models.CASCADE,
        related_name="courses"
    )
    course_url = models.URLField(max_length=1000)
    skill_level = models.CharField(
        max_length=20,
        choices=SKILL_LEVEL_CHOICES
    )
    learning_mode = models.CharField(
        max_length=20,
        choices=LEARNING_MODE_CHOICES
    )
    language = models.CharField(
        max_length=50,
        choices=LANGUAGE_CHOICES
    )
    duration = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    is_course_free = models.BooleanField(default=True)
    price = models.FloatField(
        blank=True,
        null=True
    )
    certificate_available = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    views_count = models.PositiveIntegerField(default=0)
    popularity_score = models.FloatField(default=0.0)
    updated_at = models.DateTimeField(auto_now=True)
    rating = models.FloatField(default=0.0, null=True, blank=True)
    class Meta:
        ordering = ['-popularity_score', '-created_at']
    def __str__(self):
        return f"{self.name} ({self.platform.name})"
class UserPreference(models.Model):
    SKILL_LEVEL_CHOICES = Course.SKILL_LEVEL_CHOICES
    LEARNING_MODE_CHOICES = [
        ('video', 'Video'),
        ('text', 'Text')
    ]
    LANGUAGE_CHOICES = Course.LANGUAGE_CHOICES
    PLAN_CHOICES = [
        ('free', 'Free'),
        ('paid', 'Paid')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=300)
    skill_level = models.CharField(
        max_length=20,
        choices=SKILL_LEVEL_CHOICES,
        blank=True,
        null=True
    )
    plan = models.CharField(
        max_length=20,
        choices=PLAN_CHOICES,
        blank=True,
        null=True
    )
    certification_needed = models.BooleanField(default=False)
    learning_mode = models.CharField(
        max_length=20,
        choices=LEARNING_MODE_CHOICES,
        blank=True,
        null=True
    )
    language = models.CharField(
        max_length=50,
        choices=LANGUAGE_CHOICES,
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username} - {self.course_name}"
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=255)
    #platform = models.CharField(max_length=255)
    skill_level = models.CharField(max_length=50, blank=True, null=True)
    plan = models.CharField(max_length=50, blank=True, null=True)
    language = models.CharField(max_length=50, blank=True, null=True)
    learning_mode = models.CharField(max_length=50, blank=True, null=True)
    certification_needed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
#class Favorite(models.Model):
 #   user = models.ForeignKey(User, on_delete=models.CASCADE)
  #  course = models.ForeignKey(Course, on_delete=models.CASCADE)
   # saved_at = models.DateTimeField(auto_now_add=True)
#
 #   def __str__(self):
   #     return f"{self.user.username} - {self.course.name}"
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=500, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    platform = models.CharField(max_length=100, default="YouTube")
    created_at = models.DateTimeField(auto_now_add=True)"""


from django.db import models
from django.contrib.auth.models import User
class Platform(models.Model):
    name = models.CharField(max_length=200, unique=True)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name
class Course(models.Model):
    SKILL_LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced')
    ]
    LEARNING_MODE_CHOICES = [
        ('video', 'Video'),
        ('text', 'Text'),
        ('mixed', 'Mixed')
    ]
    LANGUAGE_CHOICES = [
        ('english', 'English'),
        ('hindi', 'Hindi')
    ]
    name = models.CharField(max_length=500)
    platform = models.ForeignKey(
        'Platform',
        on_delete=models.CASCADE,
        related_name="courses"
    )
    course_url = models.URLField(max_length=1000)
    skill_level = models.CharField(
        max_length=20,
        choices=SKILL_LEVEL_CHOICES
    )
    learning_mode = models.CharField(
        max_length=20,
        choices=LEARNING_MODE_CHOICES
    )
    language = models.CharField(
        max_length=50,
        choices=LANGUAGE_CHOICES
    )
    duration = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    is_course_free = models.BooleanField(default=True)
    price = models.FloatField(
        blank=True,
        null=True
    )
    certificate_available = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    views_count = models.PositiveIntegerField(default=0)
    popularity_score = models.FloatField(default=0.0)
    updated_at = models.DateTimeField(auto_now=True)
    rating = models.FloatField(default=0.0, null=True, blank=True)
    class Meta:
        ordering = ['-popularity_score', '-created_at']
    def __str__(self):
        return f"{self.name} ({self.platform.name})"
class UserPreference(models.Model):
    SKILL_LEVEL_CHOICES = Course.SKILL_LEVEL_CHOICES
    LEARNING_MODE_CHOICES = [
        ('video', 'Video'),
        ('text', 'Text')
    ]
    LANGUAGE_CHOICES = Course.LANGUAGE_CHOICES
    PLAN_CHOICES = [
        ('free', 'Free'),
        ('paid', 'Paid')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=300)
    skill_level = models.CharField(
        max_length=20,
        choices=SKILL_LEVEL_CHOICES,
        blank=True,
        null=True
    )
    plan = models.CharField(
        max_length=20,
        choices=PLAN_CHOICES,
        blank=True,
        null=True
    )
    certification_needed = models.BooleanField(default=False)
    learning_mode = models.CharField(
        max_length=20,
        choices=LEARNING_MODE_CHOICES,
        blank=True,
        null=True
    )
    language = models.CharField(
        max_length=50,
        choices=LANGUAGE_CHOICES,
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username} - {self.course_name}"
"""class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)"""
from django.db import models
from django.contrib.auth.models import User
from .models import Course

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    course_url = models.URLField(null=True, blank=True)
    course_name = models.CharField(max_length=255, null=True, blank=True)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        if self.course:
            return f"{self.user.username} - {self.course.name}"
        return f"{self.user.username} - {self.course_name or 'External Course'}"
class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=255)
    #platform = models.CharField(max_length=255)
    skill_level = models.CharField(max_length=50, blank=True, null=True)
    plan = models.CharField(max_length=50, blank=True, null=True)
    language = models.CharField(max_length=50, blank=True, null=True)
    learning_mode = models.CharField(max_length=50, blank=True, null=True)
    certification_needed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=500, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    platform = models.CharField(max_length=100, default="YouTube")
    created_at = models.DateTimeField(auto_now_add=True)
