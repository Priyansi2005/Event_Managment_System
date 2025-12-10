from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError
from .models import Event, RSVP, Review
from .serializers import EventSerializer, RSVPSerializer, ReviewSerializer
from .permissions import IsOwnerOrReadOnly

from django.http import HttpResponse

def home(request):
    html_content = """
    <html>
    <head>
        <title>Event API</title>
        <style>
            body {
                background: linear-gradient(135deg, #6A11CB, #2575FC);
                font-family: 'Arial', sans-serif;
                margin: 0;
                padding: 0;
                color: white;
                text-align: center;
            }
            .container {
                margin-top: 15%;
            }
            h1 {
                font-size: 48px;
                margin-bottom: 10px;
            }
            p {
                font-size: 22px;
                opacity: 0.9;
            }
            .box {
                background: rgba(255, 255, 255, 0.15);
                padding: 30px;
                width: 50%;
                margin: auto;
                border-radius: 15px;
                backdrop-filter: blur(10px);
                box-shadow: 0 4px 20px rgba(0,0,0,0.2);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="box">
                <h1> Event API is Live 🚀 </h1>
                <p>Welcome to the backend of Event Management System</p>
                <p>Your API is live and ready to use!</p>
            </div>
        </div>
    </body>
    </html>
    """

    return HttpResponse(html_content)



class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]

    def perform_create(self, serializer):
        # Set the event owner automatically
        serializer.save(owner=self.request.user)



class RSVPViewSet(viewsets.ModelViewSet):
    queryset = RSVP.objects.all()
    serializer_class = RSVPSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        
        return RSVP.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        event_id = self.request.data.get("event")
        user = self.request.user

        if not event_id:
            raise ValidationError({"event": "Event ID is required."})

        
        if RSVP.objects.filter(event_id=event_id, user=user).exists():
            raise ValidationError({"detail": "You have already RSVP'd to this event."})

        serializer.save(user=user)



class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]

    def get_queryset(self):
        queryset = Review.objects.all()
        event_id = self.request.query_params.get("event")

        
        if event_id:
            queryset = queryset.filter(event_id=event_id)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
