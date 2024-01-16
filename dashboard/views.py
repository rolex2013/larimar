from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
import itertools, operator, functools
from operator import attrgetter, or_

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
    # print(companyid, current_company)

    (projects_list, projects_tasks_list) = projects_tasks(request)
    # print(projects_list, projects_tasks_list)
    docs_tasks_list = docs_tasks(request)
    (clients_tasks_list, clients_events_list) = clients_tasks_events(request)
    (feedback_tickets_list, feedback_tasks_list) = feedback_tickets_tasks(request)

    full_list = itertools.chain(projects_list, projects_tasks_list, docs_tasks_list, clients_tasks_list, clients_events_list, feedback_tickets_list, feedback_tasks_list)
    # full_list = functools.reduce(operator.or_, [projects_list, projects_tasks_list]) # это только для одной модели
    # full_list = projects_list.union(projects_tasks_list)
    # full_list = (projects_list | projects_tasks_list) # это только для одной модели

    full_list = sorted(full_list, key=attrgetter('date_for_sort'))

    # links = [{'object': 'prj_prj', 'url_name': 'my_project:tasks'},
    #          {'object': 'prj_tsk', 'url_name': 'my_project:taskcomments'},
    #          {'object': 'docs_tsk', 'url_name': 'my_doc:doctaskcomments'},
    #          {'object': 'crm_tsk', 'url_name': 'my_crm:clienttaskcomments'},
    #          {'object': 'crm_evnt', 'url_name': 'my_crm:clienteventcomments'},
    #          {'object': 'fdb_tckt', 'url_name': 'my_feedback:feedbacktasks'},
    #          {'object': 'fdb_tsk', 'url_name': 'my_feedback:feedbacktaskcomments'},
    #         ]
    links = {'prj_prj': 'my_project:tasks',
             'prj_tsk': 'my_project:taskcomments',
             'docs_tsk': 'my_doc:doctaskcomments',
             'crm_tsk': 'my_crm:clienttaskcomments',
             'crm_evnt': 'my_crm:clienteventcomments',
             'fdb_tckt': 'my_feedback:feedbacktasks',
             'fdb_tsk': 'my_feedback:feedbacktaskcomments',
             }
    # print(links.get('docs_tsk'))

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
        'full_list': full_list,
        # 'links': {'object': 'prj_prj', 'url_name': 'my_project:tasks'},
        'links': links,
    })
