from django.shortcuts import render
from django.views.generic import CreateView, UpdateView
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from datetime import datetime  # , timedelta
import json
from django.http.response import JsonResponse
from django.db.models import F

from companies.models import Company
from .models import YList, YListItem, Dict_YListFieldType
from .forms import YListForm


def ylists(request, companyid=0, pk=0):
    if companyid == 0:
        companyid = request.session["_auth_user_currentcompany_id"]
    request.session["_auth_user_currentcomponent"] = "lists"
    currentuser = request.user.id
    current_company = Company.objects.get(id=companyid)

    list_list = (
        YList.objects.filter(
            Q(author=currentuser)
            | Q(authorupdate=currentuser)
            | Q(
                members__in=[
                    currentuser,
                ]
            ),
            is_active=True,
            company=companyid,
            dateclose__isnull=True,
        )
        .select_related("company", "author", "authorupdate")
        .prefetch_related("members")
    )

    comps = request.session["_auth_user_companies_id"]
    if len(comps) > 1:
        button_company_select = _("Сменить организацию")
    if currentuser == current_company.author_id:
        button_company_create = _("Добавить")
        button_company_update = _("Изменить")
        button_list_create = _("Добавить")
    if current_company.id in comps:
        button_list_create = _("Добавить")

    return render(
        request,
        "company_detail.html",
        {
            "nodes": list_list.order_by("-dateupdate").distinct(),
            "current_company": current_company,
            "companyid": companyid,
            "user_companies": comps,
            "component_name": "lists",
            "button_company_select": button_company_select,
            "button_company_create": button_company_create,
            "button_company_update": button_company_update,
            "button_list_create": button_list_create,
        },
    )


class YListCreate(CreateView):
    model = YList
    form_class = YListForm
    # template_name = 'task_create.html'
    template_name = "object_form.html"

    def form_valid(self, form):
        form.instance.company_id = self.kwargs["companyid"]
        form.instance.author_id = self.request.user.id
        form.instance.authorupdate_id = self.request.user.id
        form.instance.fieldslist = json.dumps(
            # {"Дата": {"type": "date", "is_active": "True"}}
            {"Дата": {"type": "1"}}
        )
        self.object = form.save()  # созадём новый список
        new_item = YListItem(
            ylist_id=self.object.id,
            fieldslist=json.dumps({"Дата": ""}),
            sort=1,
            author_id=self.request.user.id,
            authorupdate_id=self.request.user.id,
        )
        new_item.save()  # создаём одну пустую запись
        # формируем строку из Участников
        memb = self.object.members.values_list("id", "username").all()
        membersstr = ""
        for mem in memb:
            membersstr = membersstr + mem[1] + ","

        return super().form_valid(form)


class YListUpdate(UpdateView):
    model = YList
    form_class = YListForm
    template_name = "object_form.html"

    def form_valid(self, form):
        form.instance.authorupdate_id = self.request.user.id
        form.instance.dateupdate = datetime.now()
        self.object = form.save()  # Записываем изменения в список
        # формируем строку из Участников
        memb = self.object.members.values_list("id", "username").all()
        membersstr = ""
        for mem in memb:
            membersstr = membersstr + mem[1] + ","

        return super().form_valid(form)


def ylist_items0(request, pk=0):
    comps = request.session["_auth_user_companies_id"]
    current_ylist = YList.objects.filter(id=pk).first()
    # k = current_ylist.fieldslist.split(',')
    # titles = dict(current_ylist.fieldslist)
    # titles = [*json.loads(current_ylist.fieldslist)]  # преобразовываем в словарь и распаковываем ключи
    # print([*titles], titles, json.dumps(titles))
    fields = json.loads(current_ylist.fieldslist)
    titles = [*fields]  # преобразовываем в словарь и распаковываем ключи

    fieldtype = Dict_YListFieldType.objects.filter(is_active=True)

    ylistitem = YListItem.objects.filter(ylist=pk, is_active=True).select_related(
        "ylist", "author", "authorupdate"
    )
    ylisttable = []
    # cnt = 0
    for yl in ylistitem:
        name = json.loads(yl.fieldslist)
        yfield = {}
        yfield["itemid"] = yl.id
        yfield["sort"] = yl.sort
        columns = []
        # yfield['id'] = str(yl.id)
        # yfield['yl'] = yl
        for title in titles:  # пробегаем по всем ключам заголовков Списка
            # if dict(fields[title])["is_active"] == "True":
            try:
                yfield[title] = name[
                    title
                ]  # если этот ключ есть в заголовках записей Списка, то присваиваем ему его значение
            except:
                yfield[title] = ""
            columns.append(title)

        ylisttable.append(yfield)
    # print(ylisttable)

    return (
        request,
        ylisttable,
        yfield,
        current_ylist,
        columns,
        comps,
        fieldtype,
        _("Изменить"),
        _("Добавить"),
    )


def ylist_items(request, pk=0):
    comps = request.session["_auth_user_companies_id"]
    current_ylist = YList.objects.filter(id=pk).first()
    # k = current_ylist.fieldslist.split(',')
    # titles = dict(current_ylist.fieldslist)
    fields = json.loads(current_ylist.fieldslist)
    titles = [*fields]  # преобразовываем в словарь и распаковываем ключи

    fieldtype = Dict_YListFieldType.objects.filter(is_active=True)

    ylistitem = YListItem.objects.filter(ylist=pk, is_active=True).select_related(
        "ylist", "author", "authorupdate"
    )
    ylisttable = []
    columns = []
    # cnt = 0
    for yl in ylistitem:
        name = json.loads(yl.fieldslist)
        # print('********', name)
        yfield = {}
        columns = []
        yfield["itemid"] = yl.id
        yfield["sort"] = yl.sort
        # print(yfield)
        for title in titles:  # пробегаем по всем ключам заголовков Списка
            # if dict(fields[title])["is_active"] == "True":
            try:
                yfield[title] = name[
                    title
                ]  # если этот ключ есть в заголовках записей Списка, то присваиваем ему его значение
            except:
                yfield[title] = ""
            columns.append(title)
            # print('+++', yfield)
        ylisttable.append(yfield)
        # print(ylisttable)

    return render(
        request,
        "ylist_detail.html",
        {
            "ylisttable": ylisttable,
            #'nodes': ylistitem,
            #'nodes': yfield,
            "current_ylist": current_ylist,
            # 'titles': titles,
            "columns": columns,
            "len_columns": len(columns),
            # 'companyid': companyid,
            "user_companies": comps,
            # 'component_name': 'lists',
            "fieldtype": fieldtype,
            # 'button_company_select': button_company_select,
            # 'button_list_create': _("Создать"),
            "button_list_update": _("Изменить"),
            "button_item_create": _("Добавить"),
        },
    )


def ylistitemactions(request):
    reread = 1

    pk = int(request.GET["pk"])
    prz = int(request.GET["prz"])
    sort = int(request.GET["sort"])

    yitem = (
        YListItem.objects.filter(id=pk)
        .select_related("ylist", "authorupdate", "author")
        .first()
    )

    print("******************** ylistitemactions ********** ", prz, pk, sort, yitem)

    if prz == 1:  # or prz == 2:
        # дублирование записи
        # для всех записей с yli.sort>=sort увеличиваем sort на единичку
        YListItem.objects.filter(ylist=yitem.ylist, sort__gte=sort).update(
            sort=F("sort") + 1
        )
        # и вставляем новую запись
        d = json.loads(yitem.ylist.fieldslist)
        # print("-----------------------------------", d.fromkeys(d, ""))
        new_item = YListItem(
            ylist=yitem.ylist,
            fieldslist=yitem.fieldslist,
            # fieldslist=json.dumps(d.fromkeys(d, "")),
            sort=sort,
            author=request.user,
            authorupdate=request.user,
        )
        new_item.save()
    elif prz == 4:
        yitem.is_active = False
        yitem.authorupdate = request.user
        yitem.dateupdate = datetime.now()
        yitem.dateclose = datetime.now()
        yitem.save()
        ylistitem = YListItem.objects.filter(
            ylist=yitem.ylist.id, is_active=True
        ).select_related("ylist", "author", "authorupdate")
        # print("... ", ylistitem)
    elif prz == 5 or prz == 6:
        # двигаем строчки вверх и вниз
        cur_sort = yitem.sort
        if prz == 5:
            target_item = YListItem.objects.filter(
                ylist=yitem.ylist, is_active=True, sort__lt=cur_sort
            ).order_by("-sort")[0]
        else:
            target_item = YListItem.objects.filter(
                ylist=yitem.ylist, is_active=True, sort__gt=cur_sort
            ).first()
        new_sort = target_item.sort
        yitem.sort = new_sort
        yitem.save()
        target_item.sort=cur_sort
        target_item.save()
    if reread == 1:
        (
            request,
            ylisttable,
            ylistitem,
            current_ylist,
            columns,
            comps,
            fieldtype,
            button_list_update,
            button_item_create,
        ) = ylist_items0(request, yitem.ylist.id)
        return render(
            request,
            "ylist_items_list.html",
            {
                "ylisttable": ylisttable,
                "nodes": ylistitem,
                "current_ylist": current_ylist,
                "columns": columns,
                "len_columns": len(columns),
                "user_companies": comps,
                "fieldtype": fieldtype,
                "button_list_update": _("Изменить"),
                "button_item_create": _("Добавить"),
            },
        )
        # return render(
        #     request,
        #     "ylist_items_list.html",
        #     {
        #         "nodes": ylistitem,
        #     },
        # )
    else:
        return render(request, "ylist_items_list.html")


def yitemcelledit(request):
    pk = int(request.GET["pk"])
    col = request.GET["col"]
    val = request.GET["val"]
    yli = YListItem.objects.filter(id=pk).first()
    name = json.loads(yli.fieldslist)
    name[col] = val
    print(
        "===+++================ celledit",
        yli.id,
        pk,
        col,
        val,
        " yli ",
        name[col],
        name,
    )
    yli.fieldslist = json.dumps(name)
    yli.dateupdate = datetime.now()
    yli.authorupdate = request.user
    yli.save()

    return render(request, "ylist_items_list.html")

def ylistcolumnactions(request):
    reread = 1

    prz = int(request.GET["prz"])
    pk = int(request.GET["pk"])
    col = int(request.GET["col"])
    col_name = request.GET["col_name"]

    print("******* ylistcolumnactions *********** ", prz, pk, col)

    yl = YList.objects.filter(id=pk).first()

    if prz == 1 or prz == 2:
        # добавляем столбец слева или справа
        col_type = request.GET["col_type"]
        # sort = int(request.GET['sort'])
        fldlst = yl.add_column(col_name, col_type, col)  # sort)
        print("====================== column insert", pk, col, yl, fldlst)
        if fldlst == "":
            return JsonResponse(
                {
                    "success": False,
                    "errmsg": 'Столбец "Новый столбец" уже существует! Переименуйте его!',
                }
            )
    elif prz == 3:
        # изменяем наименование или тип столбца
        col_type = request.GET["col_type"]
        fldlst = yl.upd_column(col_name, col_type, col)
        # reread = 0
    elif prz == 4:
        # удаляем столбец
        # print(col_name)
        fldlst = yl.del_column(col_name)
    elif prz == 5 or prz == 6:
        # переносим столбец влево или вправо
        fldlst = yl.shift_column(col, prz)

    if reread == 1:
        (
            request,
            ylisttable,
            ylistitem,
            current_ylist,
            columns,
            comps,
            fieldtype,
            button_list_update,
            button_item_create,
        ) = ylist_items0(request, yl.id)
        return render(
            request,
            "ylist_items_list.html",
            {
                "ylisttable": ylisttable,
                "nodes": ylistitem,
                "current_ylist": current_ylist,
                "columns": columns,
                "len_columns": len(columns),
                "user_companies": comps,
                "fieldtype": fieldtype,
                "button_list_update": _("Изменить"),
                "button_item_create": _("Добавить"),
            },
        )
    else:
        return render(request, "ylist_items_list.html")


def ylistfilter(request):
    pass
