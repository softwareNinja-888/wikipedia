from django.urls import path

from . import views

app_name = "wiki"

urlpatterns = [
    path("", views.index, name="index"),    
    # path("display/", views.display, name="display"),
    path("<str:title>", views.direct, name="direct"),
]
