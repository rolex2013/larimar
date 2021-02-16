import django_tables2 as tables
from .models import ProjectStatusLog, TaskStatusLog #, Project

#class Blank1Column(tables.Column):
#
#    def render(self, record):
#        return ' {}'.format(record.status)

class ProjectStatusLogTable(tables.Table):
    #blank1 = tables.Column('   ')
    #status = Blank1Column()
    #blank2 = tables.Column(' ',empty_values=[])
    #blank3 = tables.Column('   ')

    #def render_blank2(value):
    #   #if not value:
    #   #   return 'Nobody Home'
    #   return '     '

    class Meta:
        model = ProjectStatusLog
        # add class="paleblue" to <table> tag
        attrs = {'class': 'd-table'}
        exclude = ('id', 'project', 'is_active')
        order_by = '-date'        
        #sequence = ('date', 'blank1', 'status', 'blank2', 'author', 'blank3', 'description')
        sequence = ('date', 'status', 'author', 'description')

class TaskStatusLogTable(tables.Table):
    #age = tables.Column('Custom name')
    class Meta:
        model = TaskStatusLog
        # add class="paleblue" to <table> tag
        attrs = {'class': 'd-table'}
        exclude = ('id', 'task', 'is_active')
        order_by = '-date'
        sequence = ('date', 'status', 'author', 'description')   


#class ProjectTable(tables.Table):
#    class Meta:
#        model = Project
#        # add class="paleblue" to <table> tag
#        #attrs = {'class': 'paleblue'}
#        #exclude = ('id', 'is_active')
#        #sequence = ('date', 'status', 'author', 'description')             