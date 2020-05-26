from django.contrib import admin

from accounts.models import UserProfile

from main.models import Meta_ObjectType, Component, Dict_ProtocolType, Notification

from financies.models import Dict_Currency

from companies.models import Company
from companies.models import Dict_CompanyStructureType
from companies.models import Dict_CompanyType
from companies.models import UserCompanyComponentGroup
from companies.models import Dict_ContentType, Dict_ContentPlace, Content

from projects.models import Dict_ProjectStructureType, Dict_TaskStructureType
from projects.models import Dict_ProjectType, Dict_ProjectStatus, Dict_TaskType, Dict_TaskStatus
from projects.models import Project, Task, TaskComment
from projects.models import ProjectStatusLog, TaskStatusLog

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


admin.site.register(UserProfile)


admin.site.register(Meta_ObjectType)

admin.site.register(Component, ComponentAdmin)

admin.site.register(Dict_ProtocolType)

admin.site.register(Notification)


admin.site.register(Dict_Currency)


admin.site.register(Company, CompanyAdmin)

admin.site.register(UserCompanyComponentGroup)


admin.site.register(Project, ProjectAdmin)

admin.site.register(Task, TaskAdmin)

#admin.site.register(TaskComment, TaskCommentAdmin)


admin.site.register(Dict_CompanyStructureType)

admin.site.register(Dict_CompanyType)

admin.site.register(Dict_ContentType)

admin.site.register(Dict_ContentPlace)

admin.site.register(Content)


admin.site.register(Dict_ProjectStructureType)

admin.site.register(Dict_ProjectType)

admin.site.register(Dict_ProjectStatus)


admin.site.register(Dict_TaskStructureType)

admin.site.register(Dict_TaskType)

admin.site.register(Dict_TaskStatus)

admin.site.register(TaskComment)


admin.site.register(ProjectStatusLog)

admin.site.register(TaskStatusLog)

