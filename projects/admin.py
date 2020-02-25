from django.contrib import admin
from .models import Dict_CompanyStructureType, Dict_ProjectStructureType, Dict_TaskStructureType
from .models import Dict_CompanyType, Dict_ProjectType, Dict_ProjectStatus, Dict_TaskType, Dict_TaskStatus
from .models import Company, Project, Task, TaskComment
from django_mptt_admin.admin import DjangoMpttAdmin
#from models import Company

class CompanyAdmin(DjangoMpttAdmin):
    pass

class ProjectAdmin(DjangoMpttAdmin):
    pass

class TaskAdmin(DjangoMpttAdmin):
    pass

admin.site.register(Company, CompanyAdmin)

admin.site.register(Project, ProjectAdmin)

admin.site.register(Task, TaskAdmin)



admin.site.register(Dict_CompanyStructureType)

admin.site.register(Dict_CompanyType)


admin.site.register(Dict_ProjectStructureType)

admin.site.register(Dict_ProjectType)

admin.site.register(Dict_ProjectStatus)


admin.site.register(Dict_TaskStructureType)

admin.site.register(Dict_TaskType)

admin.site.register(Dict_TaskStatus)

#admin.site.register(Company)

#admin.site.register(Project)

#admin.site.register(Task)

