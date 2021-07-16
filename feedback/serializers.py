# serializers.py
from rest_framework import serializers

from .models import Dict_System, FeedbackTicket

class Dict_SystemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Dict_System
        fields = ('code', 'name', 'domain', 'url', 'ip', 'email', 'phone', 'datecreate', 'dateclose', 'is_active')

class FeedbackTicketSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FeedbackTicket
        fields = ('id_local', 'name', 'description', 'system', 'company', 'status', 'datecreate', 'dateclose', 'author', 'is_active')