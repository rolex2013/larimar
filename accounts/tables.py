import django_tables2 as tables
from main.models import Notification


class NotificationTable(tables.Table):

    class Meta:
        model = Notification
        # add class="paleblue" to <table> tag
        attrs = {'class': 'd-table'}
        exclude = ('id', 'sendfrom', 'text', 'sendto', 'datesent', 'dateread', 'type', 'is_active', 'is_read', 'is_sent', 'response', 'recipient')
        sequence = ('datecreate', 'author', 'theme')

