from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("saveListing", views.saveListing, name="saveListing"),
    path("item/<str:title>", views.item, name="item"),
    path("watchlist/<str:title>", views.add_watchlist, name="add_watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("close/<str:title>", views.close, name="close"),
    path("comment/<str:title>", views.comment, name="comment")
]
