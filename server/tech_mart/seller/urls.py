from django.urls import path


from . import views

app_name = "seller"

urlpatterns = [
    path("create/", views.create_product, name="create_product"),
]
