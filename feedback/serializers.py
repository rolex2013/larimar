# serializers.py
from rest_framework import serializers

from .models import Dict_System, FeedbackTicket
from companies.models import Company

class Dict_SystemSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="my_feedback:dict_system-detail")
    class Meta:
        model = Dict_System
        fields = ('code', 'name', 'domain', 'url', 'ip', 'email', 'phone', 'datecreate', 'dateclose', 'is_active')

class FeedbackTicketSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="my_feedback:feedbackticket-detail")
    system = serializers.HyperlinkedIdentityField(view_name="my_feedback:dict_system-detail")
    #company = serializers.HyperlinkedIdentityField(view_name="my_company:company-detail")
    company = serializers.SlugRelatedField(slug_field="name", read_only=True)
    #type = serializers.HyperlinkedIdentityField(view_name="my_feedback:dict_feedbacktype-detail")
    type = serializers.SlugRelatedField(slug_field="name", read_only=True)
    #status = serializers.HyperlinkedIdentityField(view_name="my_feedback:dict_feedbackstatus-detail")
    status = serializers.SlugRelatedField(slug_field="name", read_only=True)
    author = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = FeedbackTicket
        #fields = ('url', 'id_local', 'name', 'description', 'system', 'company', 'type', 'status', 'datecreate', 'dateclose', 'author', 'is_active')
        exclude = ('is_active',)
