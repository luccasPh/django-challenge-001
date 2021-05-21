from django.urls import path

from .views import AuthorView, CreateAuthorView, PictureAuthorView

urlpatterns = [
    path("", CreateAuthorView.as_view(), name="authors"),
    path("<str:pk>/", AuthorView.as_view(), name="authors"),
    path("<str:pk>/picture/", PictureAuthorView.as_view(), name="authors"),
]
