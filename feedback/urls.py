#from django.contrib.auth import views
from django.urls import path, include
from rest_framework import routers

#from companies.models import Company
#from .models import Dict_System, FeedbackTicket, FeedbackTicketComment, FeedbackTask, FeedbackTaskComment

from . import views

app_name = 'my_feedback'

router = routers.DefaultRouter()
router.register(r'system', views.Dict_SystemViewSet)
#router.register(r'company', views.CompanyViewSet)
router.register(r'ticket', views.FeedbackTicketViewSet)
router.register(r'ticketcomment', views.FeedbackTicketCommentViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #path('systems_page/system_reg', views.SystemCreate.as_view(), name='system_reg'),
    #path('api/system_reg', views.Dict_SystemViewSet.as_view({'get': 'create'}), name='system_reg'),
    #path('api/ticket_create', views.FeedbackTicketViewSet.as_view({'get': 'list'}), name='ticket_create'),
    #path('api/tickets', views.FeedbackTicketViewSet.as_view({'get': 'create'}), name='ticket_create'),
    #path('api/ticketcomment_create', views.FeedbackTicketCommentViewSet.as_view({'get': 'create'}), name='ticketcomment_create'),
    #path('company_detail/', views.CompanyViewSet.as_view({'get': 'create'}), name='company_detail'),

    path('system_page/system_create/', views.Dict_SystemCreate.as_view(), name='feedbacksystem_create'),
    path('tickets_page0/<int:is_ticketslist_dev>/<int:systemid>', views.feedbacktickets, name='tickets0'),
    path('tickets_page/<int:is_ticketslist_dev>/<int:systemid>/<int:companyid>', views.feedbacktickets, name='tickets'),
    #path('tickets_page0', views.feedbacktickets, name='tickets0'),
    #path('tickets_page/<int:companyid>', views.feedbacktickets, name='tickets'),
    #path('ticketsdev_page', views.feedbackticketsdev, name='ticketsdev'),   # Тикеты разработчику
    path('tickets_page/ticket_create/<int:systemid>/<int:companyid>', views.FeedbackTicketCreate.as_view(),
         name='feedbackticket_create'),
    path('tickets_page/ticket_update/<int:pk>', views.FeedbackTicketUpdate.as_view(), name='feedbackticket_update'),
    path('tickets_page/task_create/<int:ticketid>/<int:parentid>/<int:companyid>', views.FeedbackTaskCreate.as_view(), name='feedbacktask_create'),
    path('tickets_page/task_update/<int:pk>', views.FeedbackTaskUpdate.as_view(), name='feedbacktask_update'),

    path('tickettasks_page/<int:ticketid>/<int:pk>', views.feedbacktasks, name='feedbacktasks'),

    path('tickets_list/ticket_filter/', views.ticketfilter, name='ticket_filter'),
    path('tickettasks_page/task_filter/', views.tickettaskfilter, name='tickettask_filter'),

    #path('tickets_page/<int:companyid>', views.FeedbackTicketViewSet.as_view({'get': 'list'}), name='tickets'),
    #path('tickets_list/ticket_create/<int:companyid>', views.FeedbackTicketViewSet.as_view({'get': 'create'}), name='ticket_create'),
    #path('tickets_list/ticket_update/<int:pk>', views.FeedbackTicketViewSet.as_view({'get': 'update'}), name='ticket_update'),

    #path('ticketcomments_page/<int:ticketid>', views.feedbackticketcomments, name='feedbackticketcomments'),
    #path('ticketcomments_list/<int:pk>', views.FeedbackTicketCommentDetail.as_view(), name='feedbacktaskcomment_detail'),
    #path('tickets_page/ticketcomment_create/<int:ticketid>/<int:companyid>', views.FeedbackTicketCommentCreate.as_view(),
    #     name='feedbackticketcomment_create'),
    path('tickets_page/ticketcomment_create/<int:ticketid>',
         views.FeedbackTicketCommentCreate.as_view(),
         name='feedbackticketcomment_create'),
    path('tickets_page/taskcomments_page/<int:taskid>', views.feedbacktaskcomments, name='feedbacktaskcomments'),
    #path('taskcomments_list/<int:pk>', views.FeedbackTaskCommentDetail.as_view(), name='feedbacktaskcomment_detail'),
    path('tickets_page/taskcomment_create/<int:taskid>', views.FeedbackTaskCommentCreate.as_view(),
         name='feedbacktaskcomment_create'),
    #path('taskcomments_list/taskcomment_update/<int:pk>', views.FeedbackTaskCommentUpdate.as_view(), name='feedbacktaskcomment_update'),

    # Тикеты с Разработчиком
    #path('ticketsdev_page0/', views.FeedbackTicketDevCreate.as_view(), name='ticketsdev0'),
    #path('ticketsdev_page/<int:systemid>', views.feedbackticketsdev, name='ticketsdev'),
    #path('ticketsdev_page/ticketdev_create/<int:systemid>/<int:systemid>', views.FeedbackTicketDevCreate.as_view(), name='feedbackticketdev_create'),
    # ***

]
