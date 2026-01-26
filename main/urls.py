from django.urls import path
from django.contrib.auth import views as auth_views

from .forms import LoginForm
from .views import (
    add_comment,
    add_item,
    home,
    item_comments_api,
    item_detail_api,
    items_api,
    logout_view,
    register,
)


urlpatterns = [
    path("", home, name="home"),
    path("register/", register, name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="login.html",
            authentication_form=LoginForm,
        ),
        name="login",
    ),
    path("logout/", logout_view, name="logout"),
    path("add/", add_item, name="add_item"),
    path("items/<int:item_id>/comment/", add_comment, name="add_comment"),
    path("api/items/", items_api),
    path("api/items/<int:item_id>/", item_detail_api),
    path("api/items/<int:item_id>/comments/", item_comments_api),
]
