import django_tables2 as tables
from .models import Client, ClientStatusLog, ClientTaskStatusLog, ClientEventStatusLog

#class Blank1Column(tables.Column):
#
#    def render(self, record):
#        return ' {}'.format(record.status)

class ClientTable(tables.Table):

    #TEMPLATE = '''
    #           <a href="{% url some_url_edit record.pk %}" class="tbl_icon edit">Edit</a>
    #           <a href="{% url some_url_del record.pk %}" class="tbl_icon delete">Delete</a>
    #           '''
    TEMPLATE = '''<span class="hint hint--bottom hint--info" data-hint="CRM"><b><a href="{% url 'my_crm:clients' companyid record.pk %}">{{ record.firstname }} {{ record.middlename }} {{ record.lastname }}</b></span>'''
    #linkstest1 = tables.LinkColumn("user-edit", kwargs={"UserID": tables.A("pk")})
    column_link = tables.TemplateColumn(TEMPLATE, attrs = {'class': 'Клиент'})

    #def __init__(self, *args, c1_name="",**kwargs):  #will get the c1_name from where the the class will be called.
    #    super().__init__(*args, **kwargs)
    #    TEMPLATE = '''<span class="hint hint--bottom hint--info" data-hint="CRM"><b><a href="{% url 'my_crm:clients' companyid record.pk %}">{{ record.firstname }} {{ record.middlename }} {{ record.lastname }}</b></span>'''
    #    #linkstest1 = tables.LinkColumn("user-edit", kwargs={"UserID": tables.A("pk")})
    #    column_link = tables.TemplateColumn(TEMPLATE, attrs = {'class': 'Клиент'})        
    #    self.base_columns['column_link'].verbose_name = c1_name

    class Meta:
        model = Client
        # add class="paleblue" to <table> tag
        #attrs = {'class': 'paleblue'}
        attrs = {'class': 'd-table', 'column_link': 'Клиент'}
        exclude = ('id', 'company', 'is_notify', 'protocoltype', 'phone', 'email', 'description', 'dateclose', 'members', 'is_active')
        sequence = ('lastname', 'firstname', 'middlename', 'user', 'datecreate', 'type', 'status', 'author', 'manager')             

class ClientStatusLogTable(tables.Table):
    #blank1 = tables.Column('   ')
    #status = Blank1Column()
    #blank2 = tables.Column(' ',empty_values=[])
    #blank3 = tables.Column('   ')

    #def render_blank2(value):
    #   #if not value:
    #   #   return 'Nobody Home'
    #   return '     '

    class Meta:
        model = ClientStatusLog
        # add class="paleblue" to <table> tag
        attrs = {'class': 'd-table'}
        exclude = ('id', 'client', 'is_active')
        order_by = '-date'
        #sequence = ('date', 'blank1', 'status', 'blank2', 'author', 'blank3', 'description')
        sequence = ('date', 'status', 'author', 'description')

class ClientTaskStatusLogTable(tables.Table):
    #age = tables.Column('Custom name')
    class Meta:
        model = ClientTaskStatusLog
        # add class="paleblue" to <table> tag
        attrs = {'class': 'd-table'}
        exclude = ('id', 'task', 'is_active')
        order_by = '-date'
        sequence = ('date', 'status', 'author', 'description')   

class ClientEventStatusLogTable(tables.Table):
    #age = tables.Column('Custom name')
    class Meta:
        model = ClientEventStatusLog
        # add class="paleblue" to <table> tag
        attrs = {'class': 'd-table'}
        exclude = ('id', 'event', 'is_active')
        order_by = '-date'
        sequence = ('date', 'status', 'author', 'description')   
