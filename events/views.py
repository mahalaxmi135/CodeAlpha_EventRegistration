from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .models import Event, Registration


def event_list(request):
    events = Event.objects.all()

    event_data = []

    for event in events:
        event_data.append({
            "id": event.id,
            "name": event.name,
            "description": event.description,
            "date": event.date,
            "location": event.location,
            "capacity": event.capacity
        })

    return JsonResponse(event_data, safe=False)


def event_detail(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return JsonResponse(
            {"error": "Event not found"},
            status=404
        )

    return JsonResponse({
        "id": event.id,
        "name": event.name,
        "description": event.description,
        "date": event.date,
        "location": event.location,
        "capacity": event.capacity
    })


@csrf_exempt
def register_for_event(request, event_id):
    if request.method != "POST":
        return JsonResponse(
            {"error": "Only POST requests are allowed"},
            status=405
        )

    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return JsonResponse(
            {"error": "Event not found"},
            status=404
        )

    user_name = request.POST.get("user_name")
    user_email = request.POST.get("user_email")

    if not user_name or not user_email:
        return JsonResponse(
            {"error": "user_name and user_email are required"},
            status=400
        )

    registration = Registration.objects.create(
        user_name=user_name,
        user_email=user_email,
        event=event
    )

    return JsonResponse({
        "message": "Registration successful",
        "registration_id": registration.id,
        "event": event.name,
        "user_name": registration.user_name,
        "user_email": registration.user_email
    }, status=201)


def registration_list(request):
    registrations = Registration.objects.all()

    registration_data = []

    for registration in registrations:
        registration_data.append({
            "id": registration.id,
            "user_name": registration.user_name,
            "user_email": registration.user_email,
            "event": registration.event.name,
            "registered_at": registration.registered_at
        })

    return JsonResponse(registration_data, safe=False)


@csrf_exempt
def cancel_registration(request, registration_id):
    if request.method != "DELETE":
        return JsonResponse(
            {"error": "Only DELETE requests are allowed"},
            status=405
        )

    try:
        registration = Registration.objects.get(id=registration_id)
    except Registration.DoesNotExist:
        return JsonResponse(
            {"error": "Registration not found"},
            status=404
        )

    registration.delete()

    return JsonResponse({
        "message": "Registration cancelled successfully"
    })
def home(request):
    return render(request, "events/home.html")