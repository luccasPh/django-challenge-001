from django.urls import path

from .views import AdminArticleView, ListArticleView, DetailArticleView

urlpatterns = [
    path("admin/articles/", AdminArticleView.as_view(), name="admin-article"),
    path("admin/articles/<str:pk>/", AdminArticleView.as_view(), name="admin-article"),
    path("articles/", ListArticleView.as_view(), name="public-article"),
    path("articles/<str:pk>/", DetailArticleView.as_view(), name="public-article"),
]
