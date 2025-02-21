from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="chat_home"), 
    path("<int:user_id>", views.chat_view, name='chatpage'),
    path("login/", views.user_login, name='login'),
    path("register/", views.register, name='register'),
    path("logout/", views.user_logout, name='logout'),
    path("profile/", views.profile_page, name='profile'),
    path("create_group/", views.create_grp_view, name='create_group'),
    path("<str:g_name>/groups/", views.group_view, name='group_view'),
]