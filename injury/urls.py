from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),              # default page = login
    path("register/", views.register_view, name="register"),
    path("predict/", views.predict_injury, name="predict_injury"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("logout/", views.logout_view, name="logout"),
    path(
    "athlete/<int:athlete_id>/",
    views.athlete_profile,
    name="athlete_profile"
),
]