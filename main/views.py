from django.shortcuts import render
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView

from main.models import Notification, Meta_ObjectType

from django.contrib.auth.decorators import login_required

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