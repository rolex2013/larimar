import os
from django.conf import settings

from projects.models import Project, Task, TaskComment, ProjectFile
from crm.models import Client, ClientTask, ClientTaskComment, ClientFile
from docs.models import DocVerFile #, Doc, DocFile

from django.shortcuts import render, redirect, get_object_or_404

class AddFilesMixin(object):
    model = None
    model_form = None
    template = None

    def add_files(self, form, app, obj):
        # Обрабатываем файлы нового объекта
        files = form.files.getlist('files')
        #self.object = form.save() # Созадём новый объект
        #print(new_object) 
        if form.files:
           project_id = None
           client_id = None
           task_id = None
           taskcomment_id = None
           event_id = None
           eventcomment_id = None
           doc_id = None
           docver_id = None
           if app == 'project':
              if obj == 'project':
                 project_id = self.object.id              
              if obj == 'task':
                 project_id = self.object.project.id
                 task_id = self.object.id
              if obj == 'taskcomment':
                 project_id = self.object.task.project.id
                 task_id = self.object.task.id
                 taskcomment_id = self.object.id                
           elif app == 'crm':
              if obj == 'client':
                 client_id = self.object.id              
              if obj == 'task':
                 client_id = self.object.client.id
                 task_id = self.object.id
              if obj == 'taskcomment':
                 client_id = self.object.task.client.id
                 task_id = self.object.task.id
                 taskcomment_id = self.object.id
              if obj == 'event':
                 client_id = self.object.client.id
                 event_id = self.object.id
              if obj == 'eventcomment':
                 client_id = self.object.event.client.id
                 event_id = self.object.event.id
                 eventcomment_id = self.object.id
           elif app == 'doc':
              if obj == 'document':
                 doc_id = self.object.id
                 docver_id = self.object.docver
              if obj == 'task':
                 doc_id = self.object.doc.id
                 task_id = self.object.id
              if obj == 'taskcomment':
                 doc_id = self.object.task.doc.id
                 task_id = self.object.task.id
                 taskcomment_id = self.object.id
              #if obj == 'file':
              #   doc_id = self.object.doc.id
              #   task_id = self.object.id
           for f in files:
               if app == 'project':
                  fcnt = ProjectFile.objects.filter(project_id=project_id, task_id=task_id, taskcomment_id=taskcomment_id, name=f, is_active=True).count()
                  fl = ProjectFile(project_id=project_id, task_id=task_id, taskcomment_id=taskcomment_id, pfile=f)
               elif app == 'crm':                  
                  fcnt = ClientFile.objects.filter(client_id=client_id, task_id=task_id, taskcomment_id=taskcomment_id, event_id=event_id, eventcomment_id=eventcomment_id, name=f, is_active=True).count()
                  fl = ClientFile(client_id=client_id, task_id=task_id, taskcomment_id=taskcomment_id, event_id=event_id, eventcomment_id=eventcomment_id, pfile=f)
               elif app == 'doc':
                  fcnt = DocVerFile.objects.filter(doc_id=doc_id, docver_id=docver_id, name=f, is_active=True).count()
                  fl = DocVerFile(doc_id=doc_id, docver_id=docver_id, pfile=f)

               fl.author = self.request.user
               fn = f
               if fcnt:
                  f_str = str(f)
                  ext_pos = f_str.rfind('.')
                  fn = f_str[0:ext_pos] + ' (' + str(fcnt) + ')' + f_str[ext_pos:len(f_str)]
               fl.name = f
               fl.uname = fn
               fl.save()
               fullpath = os.path.join(settings.MEDIA_ROOT, str(fl.pfile))
               fl.psize = os.path.getsize(fullpath)
               fl.save()

        return True