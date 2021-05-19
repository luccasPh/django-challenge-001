from django.urls import path

from .views import SignUpUserView, LoginUserView

urlpatterns = [
    path("sign-up/", SignUpUserView.as_view(), name="sign-up"),
    path("login/", LoginUserView.as_view(), name="login"),
]
