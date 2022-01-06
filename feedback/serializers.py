# serializers.py
from rest_framework import serializers

from .models import Dict_System, FeedbackTicket, FeedbackTicketComment, FeedbackFile, Dict_FeedbackTicketStatus, Dict_FeedbackTicketType
from companies.models import Company

class Dict_SystemSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="my_feedback:dict_system-detail")
    class Meta:
        model = Dict_System
        fields = ('code', 'name', 'domain', 'url', 'ip', 'email', 'phone', 'datecreate', 'dateclose', 'is_local', 'requeststatuscode', 'is_active')

#""
#class CompanySerializer(serializers.HyperlinkedModelSerializer):
class CompanySerializer(serializers.ModelSerializer):
    #url = serializers.HyperlinkedIdentityField(view_name="my_feedback:company-detail")
    type = serializers.SlugRelatedField(slug_field="name", read_only=True)
    structure_type = serializers.SlugRelatedField(slug_field="name", read_only=True)
    parent = serializers.SlugRelatedField(slug_field="name", read_only=True)
    currency = serializers.SlugRelatedField(slug_field="symbol", read_only=True)
    class Meta:
        model = Company
        #fields = ('id', 'name', 'description', 'url', 'ip', 'email', 'phone', 'datecreate', 'dateclose', 'is_active')
        exclude = ('is_active', 'lft', 'rght', 'tree_id', 'level', 'author')
#""

class Dict_FeedbackTicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dict_FeedbackTicketType
        fields = ('name',)

#class FeedbackTicketSerializer(serializers.HyperlinkedModelSerializer):
class FeedbackTicketSerializer(serializers.ModelSerializer):
#class FeedbackTicketSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(view_name="my_feedback:feedbackticket-detail")
    system = serializers.HyperlinkedIdentityField(view_name="my_feedback:dict_system-detail")
    company = CompanySerializer(read_only=True)
    #company = serializers.SlugRelatedField(slug_field="name", read_only=True)
    type = serializers.SlugRelatedField(slug_field="name", read_only=True)
    #type = Dict_FeedbackTicketTypeSerializer(read_only=True)
    #status = serializers.HyperlinkedIdentityField(view_name="my_feedback:dict_feedbackstatus-detail")
    status = serializers.SlugRelatedField(slug_field="name", read_only=True)
    #status = serializers.RelatedField(read_only=True)
    author = serializers.SlugRelatedField(slug_field="username", read_only=True)
    class Meta:
        model = FeedbackTicket
        fields = ('url', 'id', 'name', 'description', 'system', 'company', 'type', 'status', 'datecreate', 'dateclose', 'author', 'feedbackticket_file')
        #exclude = ('is_active', 'company')

#class FeedbackTicketCommentSerializer(serializers.HyperlinkedModelSerializer):
class FeedbackTicketCommentSerializer(serializers.ModelSerializer):
    #url = serializers.HyperlinkedIdentityField(view_name="my_feedback:feedbackticketcomment-detail")
    #system = serializers.HyperlinkedIdentityField(view_name="my_company:company-detail")
    #company = serializers.HyperlinkedIdentityField(view_name="my_feedback:feedbackticket-detail")
    ticket = FeedbackTicketSerializer(read_only=True)
    #ticket = serializers.SlugRelatedField(slug_field="name", read_only=True)
    #author = serializers.SlugRelatedField(slug_field="username", read_only=True)
    #system = Dict_SystemSerializer(read_only=True)
    class Meta:
        model = FeedbackTicketComment
        fields = ('id', 'name', 'description', 'ticket_id', 'ticket')
        #exclude = ('is_active', 'time', 'cost', 'requeststatuscode')

class FeedbackFileSerializer(serializers.ModelSerializer):
    """
    name = serializers.SlugRelatedField(slug_field="name", read_only=True)
    uname = serializers.SlugRelatedField(slug_field="uniqname", read_only=True)
    ticket = serializers.SlugRelatedField(slug_field="name", read_only=True)
    ticketcomment = serializers.SlugRelatedField(slug_field="name", read_only=True)
    task = serializers.SlugRelatedField(slug_field="name", read_only=True)
    taskcomment = serializers.SlugRelatedField(slug_field="name", read_only=True)
    pfile = models.FileField(upload_to='uploads/files/feedback', blank=True, null=True, verbose_name='Файл')
    psize = models.PositiveIntegerField(editable=False, null=True, blank=True)
    datecreate = models.DateTimeField("Создан", auto_now_add=True)
    author = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.CASCADE, verbose_name="Автор")
    is_active = models.BooleanField("Активность", default=True)
    """
    #url = serializers.HyperlinkedIdentityField(view_name="my_feedback:feedbackfile-detail")
    ticket = serializers.HyperlinkedIdentityField(view_name="my_feedback:feedbackticket-detail")
    #ticket = serializers.SlugRelatedField(slug_field="name", read_only=True)
    task = serializers.SlugRelatedField(slug_field="name", read_only=True)
    taskcomment = serializers.SlugRelatedField(slug_field="name", read_only=True)
    author = serializers.SlugRelatedField(slug_field="username", read_only=True)
    class Meta:
        model = FeedbackFile
        fields = ('pfile', 'psize', 'datecreate', 'author', 'ticket', 'task', 'taskcomment')
        #exclude = ('is_active',)

"""
class Dict_FeedbackTicketStatusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Dict_FeedbackTicketStatus
        exclude = ('is_active',)

class Dict_FeedbackTicketTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Dict_FeedbackTicketType
        exclude = ('is_active',)
"""