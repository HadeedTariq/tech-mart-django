from django.urls import path


from . import views

app_name = "account"

print("requesting")

urlpatterns = [
    path("register/", views.register_user, name="register_user"),
    path("login/", views.login_user, name="login_user"),
    path("", views.get_user, name="get_user"),
    path("logout/", views.logout_user, name="logout_user"),
]
