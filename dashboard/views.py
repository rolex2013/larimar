from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _

from companies.views import get_current_company
from projects.views import projects_tasks
from docs.views import docs_tasks
from crm.views import clients_tasks_events
from feedback.views import feedback_tickets_tasks


@login_required  # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def dashboard_lists(request, companyid=0):

    if companyid == 0:
        companyid = request.session['_auth_user_currentcompany_id']
    current_company = get_current_company(companyid)
    user_companies = request.session['_auth_user_companies_id']
    #print(companyid, current_company)

    (projects_list, projects_tasks_list) = projects_tasks(request)
    #print(projects_list, projects_tasks_list)
    docs_tasks_list = docs_tasks(request)
    (clients_tasks_list, clients_events_list) = clients_tasks_events(request)
    (feedback_tickets_list, feedback_tasks_list) = feedback_tickets_tasks(request)

    return render(request, "dashboard_detail.html", {
        'component_name': 'dashboard',
        'companyid': companyid,
        'current_company': current_company,
        'user_companies': user_companies,
        'project_nodes': projects_list,
        'project_task_nodes': projects_tasks_list,
        # 'doc_nodes': docs_list,
        'doc_task_nodes': docs_tasks_list,
        # # 'client_nodes': client_list,
        'client_task_nodes': clients_tasks_list,
        'client_event_nodes': clients_events_list,
        'feedback_ticket_nodes': feedback_tickets_list,
        'feedback_task_nodes': feedback_tasks_list,
        'button_company_select': _("Сменить организацию"),
        'company_in_archive': _("Организация перемещена в архив"),
    })
