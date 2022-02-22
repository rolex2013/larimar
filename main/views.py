import os
#import socket
from django.conf import settings
from django.http import HttpResponseNotFound

from django.shortcuts import render
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView

from main.models import Notification, Meta_ObjectType, ModelLog
from projects.models import Project, Task, ProjectFile #, TaskFile
from crm.models import Client, ClientTask, ClientEvent, ClientFile
from docs.models import Doc, DocTask, DocVerFile
from files.models import Folder, FolderFile
from django.contrib.auth.models import User

from django.db.models import Q #, Count, Min, Max, Sum, Avg

from django.contrib.auth.decorators import login_required

import json


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена!</h1>')

#def accessDenided(request, exception):
#    return HttpResponseNotFound('<h1>Доступ запрещён!</h1>')


@login_required   # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
class ProjectsHome(TemplateView):
   template_name = 'main.html'

#class Home(ListView):

def notificationread(request):
    # помечаем уведомление прочитанным
    notify_id = request.GET['val']
    curr_notify = Notification.objects.get(id=notify_id)
    if curr_notify:
       curr_notify.is_read = True
       curr_notify.save(update_fields=["is_read"])
    notification_list = Notification.objects.filter(recipient_id=request.user.id, is_active=True, is_read=False, type_id=3)
    metaobjecttype_list = Meta_ObjectType.objects.filter(is_active=True)
    return render(request,  "notify_list.html", {
                                                 'notification_list': notification_list.distinct().order_by("-datecreate"),
                                                 'metaobjecttype_list': metaobjecttype_list.distinct().order_by(),
                                                }
                 )

def notificationfilter(request):

    #currentuser = request.user.id
    notificationstatus = request.GET['notificationstatus']
    notificationobjecttype = request.GET['notificationobjecttype']

    notification_list = Notification.objects.filter(recipient_id=request.user.id, is_active=True, type_id=3)
    #print('===', notificationobjecttype, notification_list)
    if notificationstatus == "2":
       notification_list = notification_list.filter(is_read=False)       
    elif notificationstatus == "3":
       notification_list = notification_list.filter(is_read=True)
    #print(notification_list)
    
    if notificationobjecttype != "0":
       notification_list = notification_list.filter(objecttype_id=notificationobjecttype)
       #print(notificationobjecttype, notification_list)

    metaobjecttype_list = Meta_ObjectType.objects.filter(is_active=True)
  
    return render(request, "notify_list.html", {
                                                'notification_list': notification_list.distinct().order_by("-datecreate"),
                                                'metaobjecttype_list': metaobjecttype_list.distinct().order_by(),
                                                'status_selectid': notificationstatus,
                                                'metaobjecttype_selectid': notificationobjecttype,
                                               }
                 )


def sidebarnotificationfilter(request):

    notificationuser = request.user.id
    #notificationuser = request.GET['notificationuser']
    notificationstatus = request.GET['notificationstatus']
    notificationobjecttype = request.GET['notificationobjecttype']

    notification_list = Notification.objects.filter(Q(recipient_id=notificationuser) | Q(author_id=notificationuser), is_active=True, type_id=3)
    #print('===', notificationuser, notificationobjecttype, notification_list)
    if notificationstatus == "2":
        notification_list = notification_list.filter(is_read=False)
    elif notificationstatus == "3":
        notification_list = notification_list.filter(is_read=True)

    if notificationobjecttype != "0":
        notification_list = notification_list.filter(objecttype_id=notificationobjecttype)

    #metaobjecttype_list = Meta_ObjectType.objects.filter(is_active=True)

    return render(request, "sidebar_notifications_list.html", {
            'nodes': notification_list.distinct().order_by("-datecreate"),
            #'metaobjecttype_list': metaobjecttype_list.distinct().order_by(),
            #'notify_status_selectid': notificationstatus,
            #'notify_metaobjecttype_selectid': notificationobjecttype,
            }
        )

@login_required   # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def objecthistory(request, objtype='prj', pk=0):

    if objtype == 'prj':
       if pk == 0:
          current_object = 0
       else:
          current_object = Project.objects.filter(id=pk).first() #Project.objects.get(id=pk)
       templatename = 'project_history.html'
    elif objtype == 'tsk':
       if pk == 0:
          current_object = 0
       else:
          current_object = Task.objects.filter(id=pk).first()
       templatename = 'task_history.html'             
    elif objtype == 'clnt':
       if pk == 0:
          current_object = 0
       else:
          current_object = Client.objects.filter(id=pk).first()
       templatename = 'client_history.html'            
    elif objtype == 'cltsk':
       if pk == 0:
          current_object = 0
       else:
          current_object = ClientTask.objects.filter(id=pk).first()
       templatename = 'clienttask_history.html'              
    elif objtype == 'clevnt':
       if pk == 0:
          current_object = 0
       else:
          current_object = ClientEvent.objects.filter(id=pk).first()
       templatename = 'clientevent_history.html'
    elif objtype == 'doc':
       if pk == 0:
          current_object = 0
       else:
          current_object = Doc.objects.filter(id=pk).first()
       templatename = 'doc_history.html'
    elif objtype == 'dctsk':
       if pk == 0:
          current_object = 0
       else:
          current_object = DocTask.objects.filter(id=pk).first()
       templatename = 'doctask_history.html'

    comps = request.session['_auth_user_companies_id']

    # формируем массив заголовков
    #row = ModelLog.objects.filter(modelobjectid=pk, is_active=True).first()
    #row = ModelLog.objects.get(modelobjectid=pk, is_active=True)
    #titles = json.loads(row.log).items()
    #print(objtype)
    nodes = ModelLog.objects.filter(componentname=objtype, modelobjectid=pk, is_active=True) #.order_by()
    #print(nodes)
    i = -1
    mas = []
    for node in nodes:
       i += 1
       mas.append(json.loads(node.log).items())
       #print(mas[i])           
       
    return render(request, templatename, {
                              #'titles': titles,
                              'nodes': nodes,
                              'mas': mas,
                              'current_object': current_object,
                              'user_companies': comps,
                              'objtype': objtype,
                              #'table': table,                                                           
                                                })  

@login_required   # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def objectfiledelete(request, objtype='prj'):
   fileid = request.GET['fileid']
   #print(fileid)
   #print(objtype)
   obj_files_rights = request.GET['obj_files_rights']
   object_message = ''
   template = 'objectfile_list.html'
   if fileid:
      if objtype[:3] == 'prj':
         fl = ProjectFile.objects.filter(id=fileid).first()
      elif objtype[:3] == 'cln':
         fl = ClientFile.objects.filter(id=fileid).first()
      elif objtype[:3] == 'doc':
         fl = DocVerFile.objects.filter(id=fileid).first()
      elif objtype[:3] == 'fld':
         fl = FolderFile.objects.filter(id=fileid).first()
      if fl.is_active == True:
         fl.is_active = False
      else:
          fl.is_active = True
      fl.save(update_fields=['is_active'])
   if objtype == 'prj':
      files = ProjectFile.objects.filter(project_id=fl.project_id, is_active=True).order_by('uname')
   elif objtype == 'prjtsk':
      files = ProjectFile.objects.filter(task_id=fl.task_id, is_active=True).order_by('uname')
   elif objtype == 'prjtskcmnt':
      files = ProjectFile.objects.filter(taskcomment_id=fl.taskcomment_id, is_active=True).order_by('uname')
   elif objtype == 'clnt':
      files = ClientFile.objects.filter(client_id=fl.client_id, is_active=True).order_by('uname')
   elif objtype == 'clnttsk':
      files = ClientFile.objects.filter(task_id=fl.task_id, is_active=True).order_by('uname')
   elif objtype == 'clnttskcmnt':
      files = ClientFile.objects.filter(taskcomment_id=fl.taskcomment_id, is_active=True).order_by('uname')
   elif objtype == 'clntevnt':
      files = ClientFile.objects.filter(event_id=fl.event_id, is_active=True).order_by('uname')
   elif objtype == 'clntevntcmnt':
      files = ClientFile.objects.filter(teventcomment_id=fl.eventcomment_id, is_active=True).order_by('uname')
   elif objtype == 'doc':
      files = DocVerFile.objects.filter(docver_id=fl.docver_id, is_active=True).order_by('uname')
   elif objtype == 'doctsk':
      files = DocVerFile.objects.filter(task_id=fl.task_id, is_active=True).order_by('uname')
   elif objtype == 'doctskcmnt':
      files = DocVerFile.objects.filter(taskcomment_id=fl.taskcomment_id, is_active=True).order_by('uname')
   elif objtype == 'fldr':
      files = FolderFile.objects.filter(folder_id=fl.folder_id, is_active=True) #.order_by('uname')
      template = 'folderfile_list.html'
   return render(request, template, {'objtype': objtype,
                                                   'files': files,
                                                   'obj_files_rights': obj_files_rights,
                                                   'object_message': object_message,
                                                   'media_path': settings.MEDIA_URL,
                                                  })

# ***
def notifications(request):

    user_list = User.objects.filter(is_active=True)
    #return render(request, 'sidebar_notifications.html', {'recipientusernameid': '10',
    #                                              }
    #              )

    return render(request, 'sidebar.html', {'user_list': user_list,
                                                  }
                  )
