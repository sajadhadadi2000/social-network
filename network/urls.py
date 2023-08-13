
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("post/<str:page>", views.post, name="post"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createpost", views.createpost, name="createpost"),
    path("profile/<str:username>", views.profile, name="profile"),
    
    path("edit/<int:id>", views.edit, name="edit"),
    path("follow/<int:user_id>", views.follow, name="follow"),
    path("like", views.like, name="like")
]
