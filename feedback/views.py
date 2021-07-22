from django.shortcuts import render

from rest_framework import viewsets

from .serializers import Dict_SystemSerializer, FeedbackTicketSerializer
from .models import Dict_System, FeedbackTicket

class Dict_SystemViewSet(viewsets.ModelViewSet):
    queryset = Dict_System.objects.all() #.order_by('name')
    serializer_class = Dict_SystemSerializer

class FeedbackTicketViewSet(viewsets.ModelViewSet):
    queryset = FeedbackTicket.objects.filter(is_active=True).order_by('-datecreate')
    serializer_class = FeedbackTicketSerializer
    #filter_fields = ('username', 'is_player', 'first_name', 'last_name', 'team', 'email',)

#def FeedbackTicketCreateAPI(request):
#    return
