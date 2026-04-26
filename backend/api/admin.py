from django.contrib import admin
from .models import Platform, Course, Review, Favorite, SearchHistory, UserPreference

admin.site.register(Platform)
admin.site.register(Course)
admin.site.register(Review)
admin.site.register(Favorite)
admin.site.register(SearchHistory)
admin.site.register(UserPreference)