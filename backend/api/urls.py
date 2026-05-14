from django.urls import path
from . import views
from .views import result_view, add_review, delete_review
urlpatterns = [
    path('', views.auth_view, name='auth'),
    path('auth/', views.auth_view, name='auth'),
    path('logout/', views.logout_view, name='logout'),
    path('save-youtube/', views.save_youtube, name='save_youtube'),
    path('home/', views.home_view, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('about/', views.about_view, name='about'),
    path('selection/', views.selection_view, name='selection'),
    path('history/', views.history_view, name='history'),
    path('delete/<int:id>/', views.delete_history, name='delete_history'),
    path('results/', result_view, name='results'),
    path('add-review/', add_review, name='add_review'),
    path('delete-review/<int:review_id>/', delete_review, name='delete_review'),
    path('mark-helpful/', views.mark_helpful, name='mark_helpful'),
    path('saved/', views.saved_view, name='saved'),
    #path('save/<int:course_id>/', views.save_course, name='save_course'),
    #path('save-course/', views.save_course, name='save_course'),
    path('save-course/', views.save_course, name='save_course'),
    path('remove-favorite/<int:id>/', views.remove_favorite, name='remove_favorite'),
]