from django.shortcuts import render
from django.views.generic import CreateView, UpdateView
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from datetime import datetime  # , timedelta
import json
from django.db.models import F

from companies.models import Company
from .models import YList, YListItem
from .forms import YListForm


def ylists(request, companyid=0, pk=0):
    if companyid == 0:
        companyid = request.session['_auth_user_currentcompany_id']
    request.session['_auth_user_currentcomponent'] = 'lists'
    currentuser = request.user.id
    current_company = Company.objects.get(id=companyid)

    list_list = YList.objects.filter(Q(author=currentuser) | Q(authorupdate=currentuser) | Q(members__in=[currentuser, ]), is_active=True,
                                     company=companyid,
                                     dateclose__isnull=True).select_related('company', 'author', 'authorupdate').prefetch_related('members')

    comps = request.session['_auth_user_companies_id']
    if len(comps) > 1:
        button_company_select = _('Сменить организацию')
    if currentuser == current_company.author_id:
        button_company_create = _('Добавить')
        button_company_update = _('Изменить')
        button_list_create = _('Добавить')
    if current_company.id in comps:
        button_list_create = _('Добавить')

    return render(request, "company_detail.html", {
        'nodes': list_list.order_by('-dateupdate').distinct(),
        'current_company': current_company,
        'companyid': companyid,
        'user_companies': comps,
        'component_name': 'lists',
        'button_company_select': button_company_select,
        'button_company_create': button_company_create,
        'button_company_update': button_company_update,
        'button_list_create': button_list_create,
    })


class YListCreate(CreateView):
    model = YList
    form_class = YListForm
    # template_name = 'task_create.html'
    template_name = 'object_form.html'

    def form_valid(self, form):
        form.instance.company_id = self.kwargs['companyid']
        form.instance.author_id = self.request.user.id
        form.instance.authorupdate_id = self.request.user.id
        self.object = form.save()  # Созадём новый список
        # формируем строку из Участников
        memb = self.object.members.values_list('id', 'username').all()
        membersstr = ''
        for mem in memb:
            membersstr = membersstr + mem[1] + ','

        return super().form_valid(form)


class YListUpdate(UpdateView):
    model = YList
    form_class = YListForm
    template_name = 'object_form.html'

    def form_valid(self, form):
        form.instance.authorupdate_id = self.request.user.id
        form.instance.dateupdate = datetime.now()
        self.object = form.save()  # Записываем изменения в список
        # формируем строку из Участников
        memb = self.object.members.values_list('id', 'username').all()
        membersstr = ''
        for mem in memb:
            membersstr = membersstr + mem[1] + ','

        return super().form_valid(form)


def ylist_items0(request, pk=0):
    comps = request.session['_auth_user_companies_id']
    current_ylist = YList.objects.filter(id=pk).first()
    #k = current_ylist.fieldslist.split(',')
    # titles = dict(current_ylist.fieldslist)
    titles = [*json.loads(current_ylist.fieldslist)]  # преобразовываем в словарь и распаковываем ключи
    # print([*titles], titles, json.dumps(titles))

    ylistitem = YListItem.objects.filter(ylist=pk, is_active=True).select_related('ylist', 'author', 'authorupdate')
    ylisttable = []
    #cnt = 0
    for yl in ylistitem:
        name = json.loads(yl.fieldslist)
        yfield = {}
        #yfield['id'] = str(yl.id)
        yfield['yl'] = yl
        for title in titles:    # пробегаем по всем ключам заголовков Списка
            try:
                yfield[title] = name[title]     # если этот ключ есть в заголовках записей Списка, то присваиваем ему его значение
            except:
                yfield[title] = ''

            #print('=========', yl.fieldslist)
            #print(title, name, yfield)
        ylisttable.append(yfield)
    #print(ylisttable)

    return request, ylisttable, ylistitem, current_ylist, titles, comps, _("Изменить"), _("Добавить")


def ylist_items(request, pk=0):
    comps = request.session['_auth_user_companies_id']
    current_ylist = YList.objects.filter(id=pk).first()
    #k = current_ylist.fieldslist.split(',')
    # titles = dict(current_ylist.fieldslist)
    titles = [*json.loads(current_ylist.fieldslist)]  # преобразовываем в словарь и распаковываем ключи
    # print([*titles], titles, json.dumps(titles))

    ylistitem = YListItem.objects.filter(ylist=pk, is_active=True).select_related('ylist', 'author', 'authorupdate')
    ylisttable = []
    #cnt = 0
    for yl in ylistitem:
        name = json.loads(yl.fieldslist)
        yfield = {}
        #yfield['id'] = str(yl.id)
        yfield['yl'] = yl
        for title in titles:    # пробегаем по всем ключам заголовков Списка
            try:
                yfield[title] = name[title]     # если этот ключ есть в заголовках записей Списка, то присваиваем ему его значение
            except:
                yfield[title] = ''

            #print('=========', yl.fieldslist)
            #print(title, name, yfield)
        ylisttable.append(yfield)
    #print(ylisttable)

    return render(request, "ylist_detail.html", {
        'ylisttable': ylisttable,
        'nodes': ylistitem,
        'current_ylist': current_ylist,
        'titles': titles,
        # 'companyid': companyid,
        'user_companies': comps,
        # 'component_name': 'lists',
        # 'button_company_select': button_company_select,
        # 'button_list_create': _("Создать"),
        'button_list_update': _("Изменить"),
        'button_item_create': _("Добавить"),
    })


# def yitemedit(request, prz=1, pk=1, sort=1):
def yiteminsert(request):

    # prz = int(request.GET['prz'])
    pk = int(request.GET['pk'])
    sort = int(request.GET['sort'])

    yli = YListItem.objects.filter(id=pk).first()
    print('====================== insert', pk, sort, yli.ylist.id)

    # для всех записей с yli.sort>=sort увеличиваем sort на единичку
    YListItem.objects.filter(ylist=yli.ylist, sort__gte=sort).update(sort=F('sort') + 1)
    # и вставляем новую запись
    new_item = YListItem(ylist=yli.ylist, fieldslist=yli.fieldslist, sort=sort, author=request.user, authorupdate=request.user)
    new_item.save()

    (request, ylisttable, ylistitem, current_ylist, titles, comps, button_list_update, button_item_create) = ylist_items0(
        request, yli.ylist.id)

    #return render(request, 'ylist_items_list.html', {'nodes': nodes, 'object_list': 'task_list', 'object_message': object_message})
    return render(request, 'ylist_items_list.html', {
        'ylisttable': ylisttable,
        'nodes': ylistitem,
        'current_ylist': current_ylist,
        'titles': titles,
        'user_companies': comps,
        'button_list_update': _("Изменить"),
        'button_item_create': _("Добавить"),
    })

def yitemdelete(request):

    pk = int(request.GET['pk'])
    yli = YListItem.objects.filter(id=pk) #.first()
    print('====================== delete', pk)
    yli.update(is_active=False)

    return render(request, 'ylist_items_list.html')

def yitemcelledit(request):

    pk = int(request.GET['pk'])
    col = int(request.GET['col'])
    # yli = YListItem.objects.filter(id=pk) #.first()
    print('====================== celledit', pk, col)
    # yli.update(is_active=False)

    return render(request, 'ylist_items_list.html')

def ylistfilter(request):
    pass