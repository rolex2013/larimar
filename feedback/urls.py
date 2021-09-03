#from django.contrib.auth import views
from django.urls import path, include
from rest_framework import routers

from companies.models import Company
from .models import Dict_System, FeedbackTicket, FeedbackTicketComment, FeedbackTask, FeedbackTaskComment

from . import views

app_name = 'my_feedback'

router = routers.DefaultRouter()
router.register(r'system', views.Dict_SystemViewSet)
router.register(r'ticket', views.FeedbackTicketViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #path('systems_page/system_reg', views.SystemCreate.as_view(), name='system_reg'),
    path('systems_page/system_reg', views.Dict_SystemViewSet.as_view({'get': 'create'}), name='system_reg'),
    path('tickets_page0/', views.feedbacktickets, name='tickets0'),
    path('tickets_page/<int:companyid>/<int:pk>', views.feedbacktickets, name='tickets'),
    path('tickets_page/ticket_create/<int:systemid>/<int:companyid>', views.FeedbackTicketCreate.as_view(),
         name='feedbackticket_create'),
    #path('tickets_page/ticket_create/<int:systemid>/<int:companyid>/<int:pk>', views.TicketUpdate.as_view(),
    #     name='ticket_update'),
    #path('tickets_list/ticket_filter/', views.ticketfilter, name='ticket_filter'),

    #path('tickets_page/<int:companyid>', views.FeedbackTicketViewSet.as_view({'get': 'list'}), name='tickets'),
    #path('tickets_list/ticket_create/<int:companyid>', views.FeedbackTicketViewSet.as_view({'get': 'create'}), name='ticket_create'),
    #path('tickets_list/ticket_update/<int:pk>', views.FeedbackTicketViewSet.as_view({'get': 'update'}), name='ticket_update'),

]
