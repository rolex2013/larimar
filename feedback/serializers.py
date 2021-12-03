# serializers.py
from rest_framework import serializers

from .models import Dict_System, FeedbackTicket, FeedbackTicketComment, Dict_FeedbackTicketStatus, Dict_FeedbackTicketType
from companies.models import Company

class Dict_SystemSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="my_feedback:dict_system-detail")
    class Meta:
        model = Dict_System
        fields = ('code', 'name', 'domain', 'url', 'ip', 'email', 'phone', 'datecreate', 'dateclose', 'is_local', 'requeststatuscode', 'is_active')

class CompanySerializer(serializers.HyperlinkedModelSerializer):
    #url = serializers.HyperlinkedIdentityField(view_name="company_detail", lookup_field='name', read_only=True)
    class Meta:
        model = Company
        #fields = ('code', 'name', 'domain', 'url', 'ip', 'email', 'phone', 'datecreate', 'dateclose', 'is_active')
        exclude = ('is_active',)

class FeedbackTicketSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="my_feedback:feedbackticket-detail")
    system = serializers.HyperlinkedIdentityField(view_name="my_feedback:dict_system-detail")
    #company = serializers.HyperlinkedRelatedField(view_name="my_company:company_detail", lookup_field='name', read_only=True)
    company = CompanySerializer()
    #company = serializers.SlugRelatedField(slug_field="name", read_only=True)
    #type = serializers.HyperlinkedIdentityField(view_name="my_feedback:dict_feedbacktype-detail")
    type = serializers.SlugRelatedField(slug_field="name", read_only=True)
    #status = serializers.HyperlinkedIdentityField(view_name="my_feedback:dict_feedbackstatus-detail")
    status = serializers.SlugRelatedField(slug_field="name", read_only=True)
    author = serializers.SlugRelatedField(slug_field="username", read_only=True)
    class Meta:
        model = FeedbackTicket
        #fields = ('url', 'id_local', 'name', 'description', 'system', 'company', 'type', 'status', 'datecreate', 'dateclose', 'author', 'is_active')
        exclude = ('is_active',)

class FeedbackTicketCommentSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="my_feedback:feedbackticketcomment-detail")
    system = serializers.HyperlinkedIdentityField(view_name="my_feedback:dict_system-detail")
    ticket = serializers.SlugRelatedField(slug_field="name", read_only=True)
    author = serializers.SlugRelatedField(slug_field="username", read_only=True)
    class Meta:
        model = FeedbackTicketComment
        exclude = ('is_active',)

class Dict_FeedbackTicketStatusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Dict_FeedbackTicketStatus
        exclude = ('is_active',)

class Dict_FeedbackTicketTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Dict_FeedbackTicketType
        exclude = ('is_active',)