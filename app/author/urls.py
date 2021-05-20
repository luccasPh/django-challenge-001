from django.urls import path

from .views import DetailAuthorView, CreateAuthorView, UploadAuthorView

urlpatterns = [
    path("author/", CreateAuthorView.as_view(), name="author"),
    path("author/<str:pk>", DetailAuthorView.as_view(), name="author"),
    path("author/<str:pk>/upload", UploadAuthorView.as_view(), name="author"),
]
