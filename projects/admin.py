from django.contrib import admin

from accounts.models import UserProfile

from main.models import Meta_ObjectType, Component, Dict_ProtocolType, Notification, Menu, MenuItem

from finance.models import Dict_Currency, CurrencyRate

from companies.models import Company
from companies.models import Dict_CompanyStructureType
from companies.models import Dict_CompanyType
from companies.models import UserCompanyComponentGroup
from companies.models import Dict_ContentType, Dict_ContentPlace, Content
from companies.models import Dict_PositionType, StaffList, Staff, Summary

from projects.models import Dict_ProjectStructureType, Dict_TaskStructureType
from projects.models import Dict_ProjectType, Dict_ProjectStatus, Dict_TaskType, Dict_TaskStatus
from projects.models import Project, Task, TaskComment, ProjectFile
#from projects.models import ProjectStatusLog, TaskStatusLog

from crm.models import Dict_ClientTaskStructureType
from crm.models import Dict_ClientType, Dict_ClientStatus, Dict_ClientTaskType, Dict_ClientTaskStatus
from crm.models import Dict_ClientEventType, Dict_ClientEventStatus
from crm.models import Client, ClientTask, ClientTaskComment
#from crm.models import ClientStatusLog, ClientTaskStatusLog
from crm.models import ClientEvent, ClientEventComment
#from crm.models import ClientEventStatusLog

from django_mptt_admin.admin import DjangoMpttAdmin


class CompanyAdmin(DjangoMpttAdmin):
    pass

class ProjectAdmin(DjangoMpttAdmin):
    pass

class TaskAdmin(DjangoMpttAdmin):
    pass

#class TaskCommentAdmin(DjangoMpttAdmin):
#    pass

class ComponentAdmin(DjangoMpttAdmin):
    pass

class MenuItemAdmin(DjangoMpttAdmin):
    pass

class StaffListAdmin(DjangoMpttAdmin):
    pass

class ClientTaskAdmin(DjangoMpttAdmin):
    pass



admin.site.register(UserProfile)


admin.site.register(Meta_ObjectType)

admin.site.register(Component, ComponentAdmin)

admin.site.register(Dict_ProtocolType)

admin.site.register(Notification)

admin.site.register(Menu)

admin.site.register(MenuItem, MenuItemAdmin)


admin.site.register(Dict_Currency)

admin.site.register(CurrencyRate)


admin.site.register(Company, CompanyAdmin)

admin.site.register(UserCompanyComponentGroup)


admin.site.register(Project, ProjectAdmin)

admin.site.register(Task, TaskAdmin)

admin.site.register(ClientTask, ClientTaskAdmin)

#admin.site.register(TaskComment, TaskCommentAdmin)

# company

admin.site.register(Dict_CompanyStructureType)

admin.site.register(Dict_CompanyType)

admin.site.register(Dict_PositionType)

admin.site.register(StaffList, StaffListAdmin)

admin.site.register(Staff)

admin.site.register(Summary)

admin.site.register(Dict_ContentType)

admin.site.register(Dict_ContentPlace)

admin.site.register(Content)

# projects

admin.site.register(Dict_ProjectStructureType)

admin.site.register(Dict_ProjectType)

admin.site.register(Dict_ProjectStatus)

admin.site.register(Dict_TaskStructureType)

admin.site.register(Dict_TaskType)

admin.site.register(Dict_TaskStatus)

admin.site.register(TaskComment)

admin.site.register(ProjectFile)

#admin.site.register(ProjectStatusLog)

#admin.site.register(TaskStatusLog)

# crm

admin.site.register(Dict_ClientType)

admin.site.register(Dict_ClientStatus)

admin.site.register(Dict_ClientTaskStructureType)

admin.site.register(Dict_ClientTaskType)

admin.site.register(Dict_ClientTaskStatus)

admin.site.register(Dict_ClientEventType)

admin.site.register(Dict_ClientEventStatus)

admin.site.register(Client)

admin.site.register(ClientEvent)

admin.site.register(ClientTaskComment)

admin.site.register(ClientEventComment)

#admin.site.register(ClientStatusLog)

#admin.site.register(ClientTaskStatusLog)

#admin.site.register(ClientEventStatusLog)