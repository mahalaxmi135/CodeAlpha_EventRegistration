from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.home, name="home"),

    path("", views.event_list, name="event-list"),

    path("<int:event_id>/", views.event_detail, name="event-detail"),

    path(
        "<int:event_id>/register/",
        views.register_for_event,
        name="register-event"
    ),

    path(
        "registrations/",
        views.registration_list,
        name="registration-list"
    ),

    path(
        "registrations/<int:registration_id>/",
        views.cancel_registration,
        name="cancel-registration"
    ),
]