from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_page, name='profile_page'),
    path('activity/', views.activity, name='activity'),
    path('answers/', views.answers_page, name='answers_page'),
    path('questions/', views.questions_page, name='questions_page'),
    path('tags/', views.tags_page, name='tags_page'),
    path('editprofile/', views.edit_profile, name='edit_profile'),
    path('saved/', views.saved_page, name='saved_page'),
    path('is-saved/<int:pk>', views.is_saved, name='is_saved'),
    path('delete_saved/<int:pk>', views.deleteSaved, name='delete_saved'),
]
