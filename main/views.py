from django.shortcuts import render
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView

from main.models import Notification, Meta_ObjectType, ModelLog
from projects.models import Project, Task
from crm.models import Client, ClientTask, ClientEvent

from django.contrib.auth.decorators import login_required

import json


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
       curr_notify.save()
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

    notification_list = Notification.objects.filter(recipient_id=request.user.id, is_active=True)
    if notificationstatus == "2":
       notification_list = notification_list.filter(is_read=False)       
    elif notificationstatus == "3":
       notification_list = notification_list.filter(is_read=True)
    #print(notification_list)
    
    if notificationobjecttype != "0":
       notification_list = notification_list.filter(objecttype_id=notificationobjecttype)

    metaobjecttype_list = Meta_ObjectType.objects.filter(is_active=True)
  
    return render(request, "notify_list.html", {
                                                'notification_list': notification_list.distinct().order_by("-datecreate"),
                                                'metaobjecttype_list': metaobjecttype_list.distinct().order_by(),
                                                'status_selectid': notificationstatus,
                                                'metaobjecttype_selectid': notificationobjecttype,
                                               }
                 )    

@login_required   # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def objecthistory(request, objtype='prj', pk=0):

    if objtype == 'prj':
       if pk == 0:
          current_object = 0
       else:
          current_object = Project.objects.get(id=pk)
       templatename = 'project_history.html'
    elif objtype == 'tsk':
       if pk == 0:
          current_object = 0
       else:
          current_object = Task.objects.get(id=pk)
       templatename = 'task_history.html'             
    elif objtype == 'clnt':
       if pk == 0:
          current_object = 0
       else:
          current_object = Client.objects.get(id=pk)
       templatename = 'client_history.html'            
    elif objtype == 'cltsk':
       if pk == 0:
          current_object = 0
       else:
          current_object = ClientTask.objects.get(id=pk)
       templatename = 'clienttask_history.html'              
    elif objtype == 'clevnt':
       if pk == 0:
          current_object = 0
       else:
          current_object = ClientEvent.objects.get(id=pk)
       templatename = 'clientevent_history.html'             

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
                              'current_object':current_object,
                              'user_companies': comps,
                              #'table': table,                                                           
                                                })  
     