from django.urls import include, path

urlpatterns = [
    path("", include("masking.urls")),
]
