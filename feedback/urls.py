#from django.contrib.auth import views
from django.urls import path, include
from rest_framework import routers

#from companies.models import Company
#from .models import Dict_System, FeedbackTicket, FeedbackTicketComment, FeedbackTask, FeedbackTaskComment

from . import views
#from companies.views import CompanyDetail

app_name = 'my_feedback'

router = routers.DefaultRouter()
router.register(r'system', views.Dict_SystemViewSet)
#router.register(r'company', views.CompanyViewSet)
router.register(r'ticket', views.FeedbackTicketViewSet)
router.register(r'ticketcomment', views.FeedbackTicketCommentViewSet)
router.register(r'file', views.FeedbackFileViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('system_page/system_create/', views.Dict_SystemCreate.as_view(), name='feedbacksystem_create'),
    path('tickets_page0/<int:is_ticketslist_dev>/<int:systemid>', views.feedbacktickets, name='tickets0'),
    path('tickets_page/<int:is_ticketslist_dev>/<int:systemid>/<int:companyid>', views.feedbacktickets, name='tickets'),

    path('tickets_page/ticket_create/<int:systemid>/<int:companyid>', views.FeedbackTicketCreate.as_view(),
         name='feedbackticket_create'),
    path('tickets_page/ticket_update/<int:pk>', views.FeedbackTicketUpdate.as_view(), name='feedbackticket_update'),
    path('tickets_page/task_create/<int:ticketid>/<int:parentid>/<int:companyid>', views.FeedbackTaskCreate.as_view(), name='feedbacktask_create'),
    path('tickets_page/task_update/<int:pk>', views.FeedbackTaskUpdate.as_view(), name='feedbacktask_update'),

    path('tickettasks_page/<int:is_ticketslist_dev>/<int:ticketid>/<int:pk>', views.feedbacktasks, name='feedbacktasks'),

    path('tickets_list/ticket_filter/', views.ticketfilter, name='ticket_filter'),
    path('tickettasks_page/task_filter/', views.tickettaskfilter, name='tickettask_filter'),

    path('tickets_page/ticketcomment_create/<int:is_ticketslist_dev>/<int:ticketid>', views.FeedbackTicketCommentCreate.as_view(), name='feedbackticketcomment_create'),
    path('tickets_page/taskcomments_page/<int:taskid>', views.feedbacktaskcomments, name='feedbacktaskcomments'),
    path('tickets_page/taskcomment_create/<int:taskid>', views.FeedbackTaskCommentCreate.as_view(), name='feedbacktaskcomment_create'),

]
