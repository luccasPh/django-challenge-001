from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(title="Django Challenge", default_version="v1"),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path("api/", include("user.urls")),
    path("api/admin/authors/", include("author.urls")),
    path("api/", include("article.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [
        path("api/docs", schema_view.with_ui("swagger", cache_timeout=0)),
    ]