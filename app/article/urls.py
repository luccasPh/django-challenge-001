from django.urls import path

from .views import AdminArticleView, ListArticleView, DetailArticleView

urlpatterns = [
    path("admin/articles/", AdminArticleView.as_view(), name="article-admin"),
    path("admin/articles/<str:pk>/", AdminArticleView.as_view(), name="article-admin"),
    path("articles/", ListArticleView.as_view(), name="article-public"),
    path("articles/<str:pk>/", DetailArticleView.as_view(), name="article-public"),
]
