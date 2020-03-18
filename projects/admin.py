from django.contrib import admin

from companies.models import Company
from companies.models import Dict_CompanyStructureType
from companies.models import Dict_CompanyType
from companies.models import UserCompany

from projects.models import Dict_ProjectStructureType, Dict_TaskStructureType
from projects.models import Dict_ProjectType, Dict_ProjectStatus, Dict_TaskType, Dict_TaskStatus
from projects.models import Project, Task, TaskComment
from projects.models import ProjectTaskStatusLog

from django_mptt_admin.admin import DjangoMpttAdmin


class CompanyAdmin(DjangoMpttAdmin):
    pass

class ProjectAdmin(DjangoMpttAdmin):
    pass

class TaskAdmin(DjangoMpttAdmin):
    pass

#class TaskCommentAdmin(DjangoMpttAdmin):
#    pass

admin.site.register(Company, CompanyAdmin)

admin.site.register(UserCompany)


admin.site.register(Project, ProjectAdmin)

admin.site.register(Task, TaskAdmin)

#admin.site.register(TaskComment, TaskCommentAdmin)


admin.site.register(Dict_CompanyStructureType)

admin.site.register(Dict_CompanyType)


admin.site.register(Dict_ProjectStructureType)

admin.site.register(Dict_ProjectType)

admin.site.register(Dict_ProjectStatus)


admin.site.register(Dict_TaskStructureType)

admin.site.register(Dict_TaskType)

admin.site.register(Dict_TaskStatus)

admin.site.register(TaskComment)


admin.site.register(ProjectTaskStatusLog)

