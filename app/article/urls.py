from django.urls import path

from .views import AdminArticleView

urlpatterns = [
    path("admin/articles/", AdminArticleView.as_view(), name="article-admin"),
    path("admin/articles/<str:pk>", AdminArticleView.as_view(), name="article-admin"),
]
