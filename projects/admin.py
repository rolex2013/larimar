from django.contrib import admin

from accounts.models import UserProfile

from main.models import Meta_ObjectType, Component, Dict_ProtocolType, Dict_Theme, Notification, Menu, MenuItem

from finance.models import Dict_Currency, CurrencyRate

from companies.models import Company
from companies.models import Dict_CompanyStructureType
from companies.models import Dict_CompanyType
from companies.models import UserCompanyComponentGroup
from companies.models import Dict_ContentType, Dict_ContentPlace, Content
from companies.models import Dict_PositionType, StaffList, Staff, Summary

from projects.models import Dict_ProjectStructureType, Dict_TaskStructureType
from projects.models import Dict_ProjectType, Dict_ProjectStatus, Dict_TaskType, Dict_TaskStatus
#from projects.models import Project, Task, TaskComment, ProjectFile
#from projects.models import ProjectStatusLog, TaskStatusLog

from crm.models import Dict_ClientTaskStructureType
from crm.models import Dict_ClientType, Dict_ClientStatus, Dict_ClientTaskType, Dict_ClientTaskStatus, Dict_ClientInitiator
from crm.models import Dict_ClientEventType, Dict_ClientEventStatus
from crm.models import Client, ClientTask, ClientTaskComment
#from crm.models import ClientStatusLog, ClientTaskStatusLog
from crm.models import ClientEvent, ClientEventComment
#from crm.models import ClientEventStatusLog

from docs.models import Dict_DocType, Dict_DocStatus, Dict_DocTaskStatus, Dict_DocTaskType
from docs.models import Doc, DocVer
from docs.models import DocTask, DocTaskComment

from files.models import Dict_FolderType, Folder

from feedback.models import Dict_System, Dict_FeedbackTicketStatus, Dict_FeedbackTicketType, Dict_FeedbackTaskStatus, FeedbackTicket

from chats.models import Dict_ChatType, Chat, ChatMember

from lists.models import Dict_YListFieldType

from django_mptt_admin.admin import DjangoMpttAdmin

#from modeltranslation.admin import TranslationAdmin, TabbedTranslationAdmin


class CompanyAdmin(DjangoMpttAdmin):
    pass

#class ProjectAdmin(DjangoMpttAdmin):
#    pass

#class TaskAdmin(DjangoMpttAdmin):
#    pass

#class TaskCommentAdmin(DjangoMpttAdmin):
#    pass

class ComponentAdmin(DjangoMpttAdmin):
    pass

class MenuItemAdmin(DjangoMpttAdmin):
    pass

class Dict_ThemeAdmin(DjangoMpttAdmin):
    pass

class StaffListAdmin(DjangoMpttAdmin):
    pass

#class ClientTaskAdmin(DjangoMpttAdmin):
#    pass

#class FolderAdmin(DjangoMpttAdmin):
#    pass


admin.site.register(UserProfile)


admin.site.register(Meta_ObjectType)

admin.site.register(Component, ComponentAdmin)

admin.site.register(Dict_ProtocolType)

admin.site.register(Dict_Theme, Dict_ThemeAdmin)

#admin.site.register(Notification)

admin.site.register(Menu)

admin.site.register(MenuItem, MenuItemAdmin)

#class Dict_CurrencyAdmin(TabbedTranslationAdmin):
#    pass

admin.site.register(Dict_Currency) #, Dict_CurrencyAdmin)

admin.site.register(CurrencyRate)


admin.site.register(Company, CompanyAdmin)

admin.site.register(UserCompanyComponentGroup)


#admin.site.register(Project, ProjectAdmin)

#admin.site.register(Task, TaskAdmin)

#admin.site.register(ClientTask, ClientTaskAdmin)

#admin.site.register(TaskComment, TaskCommentAdmin)

# company

admin.site.register(Dict_CompanyStructureType)

admin.site.register(Dict_CompanyType)

admin.site.register(Dict_PositionType)

admin.site.register(StaffList, StaffListAdmin) #

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

#admin.site.register(TaskComment)

#admin.site.register(ProjectFile)

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

admin.site.register(Dict_ClientInitiator)

#admin.site.register(Client)

#admin.site.register(ClientEvent)

#admin.site.register(ClientTaskComment)

#admin.site.register(ClientEventComment)

#admin.site.register(ClientStatusLog)

#admin.site.register(ClientTaskStatusLog)

#admin.site.register(ClientEventStatusLog)

# docs

admin.site.register(Dict_DocType)

admin.site.register(Dict_DocStatus)

admin.site.register(Dict_DocTaskType)

admin.site.register(Dict_DocTaskStatus)

#admin.site.register(Doc)

#admin.site.register(DocVer)

#admin.site.register(DocTask)

#admin.site.register(DocTaskComment)

# files

admin.site.register(Dict_FolderType)

#admin.site.register(Folder, FolderAdmin)

# feedback

admin.site.register(Dict_System)

admin.site.register(Dict_FeedbackTicketType)

admin.site.register(Dict_FeedbackTicketStatus)

admin.site.register(Dict_FeedbackTaskStatus)

#admin.site.register(FeedbackTicket)

# chats

admin.site.register(Dict_ChatType)

admin.site.register(Chat)

admin.site.register(ChatMember)

# lists

admin.site.register(Dict_YListFieldType)
