from django.conf import settings
from django.urls import reverse, reverse_lazy
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count, Min, Max, Sum, Avg

from django.utils.translation import gettext_lazy as _

from django.views.generic import (
    View,
    TemplateView,
    ListView,
    DetailView,
    CreateView,
    FormView,
)
from django.views.generic.edit import UpdateView

from main.utils import AddFilesMixin  # ObjectUpdateMixin

from main.models import Dict_Theme
from companies.models import Company

from files.models import Folder, FolderFile, Dict_FolderType

from .forms import FolderForm, UploadFilesForm


@login_required  # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def folders(request, companyid=0, pk=0):
    if companyid == 0:
        companyid = request.session["_auth_user_currentcompany_id"]

    request.session["_auth_user_currentcomponent"] = "files"

    # *** фильтруем по тематике ***
    currentuser = request.user.id
    theme_selectid = 0
    try:
        themeid = request.POST["theme"]
    except:
        # folder_list = Folder.objects.filter(Q(author=request.user.id), is_active=True, company=companyid)
        folder_list = Folder.objects.filter(is_active=True, company=companyid)
    else:
        if themeid == "0":
            # если в выпадающем списке выбрано "Все активные"
            # folder_list = Folder.objects.filter(Q(author=request.user.id), is_active=True, company=companyid)
            folder_list = Folder.objects.filter(is_active=True, company=companyid)
        else:
            if themeid == "-1":
                # если в выпадающем списке выбрано "Все"
                # folder_list = Folder.objects.filter(Q(author=request.user.id), is_active=True, company=companyid)
                folder_list = Folder.objects.filter(is_active=True, company=companyid)
            else:
                # folder_list = Folder.objects.filter(Q(author=request.user.id), is_active=True, company=companyid, theme=themeid) #, dateclose__isnull=True)
                folder_list = Folder.objects.filter(
                    is_active=True, company=companyid, theme=themeid
                )
        theme_selectid = themeid
    # prjstatus_myselectid = myprjstatus
    # *******************************
    type_selectid = 0
    # myprjstatus = 0 # для фильтра "Мои проекты"
    try:
        typeid = request.POST["typeid"]
    except:
        folder_list = folder_list
    else:
        if typeid != "-1":
            folder_list = folder_list.filter(type=typeid)
        fldrtype_selectid = type
    # *******************************
    # project_list = project_list.order_by('dateclose')
    folder_list = folder_list.select_related("author", "company", "theme", "type")

    current_company = (
        Company.objects.filter(id=companyid)
        .select_related("author", "structure_type", "type", "currency")
        .first()
    )

    obj_files_rights = 0

    if pk == 0:
        current_folder = 0
        tree_folder_id = 0
        root_folder_id = 0
        # tree_project_id = 0
        template = "company_detail.html"
    else:
        current_folder = (
            Folder.objects.filter(id=pk)
            .select_related("author", "company", "theme", "type")
            .first()
        )
        print("******************", pk, current_folder)
        # idpk = 'id=pk'
        # current_folder = Folder.objects.get({idpk})
        tree_folder_id = current_folder.tree_id
        root_folder_id = current_folder.get_root().id
        # tree_folder_id = current_folder.tree_id
        folder_list = current_folder.get_children().filter(is_active=True)
        # folder_list = folder_list.filter(is_active=True)
        if (
            currentuser == current_folder.author_id
        ):  # or currentuser == current_folder.assigner_id:
            obj_files_rights = 1
        template = "folder_detail.html"

    len_list = len(folder_list)

    button_company_select = ""
    button_company_create = ""
    button_company_update = ""
    button_folder_create = ""
    button_folder_update = ""
    button_file_create = ""

    # здесь нужно условие для button_company_create
    # если текущий пользователь не является автором созданной текущей организации, то добавлять и изменять Компанию можно только в приложении Организации
    # button_company_create = 'Добавить'
    # здесь нужно условие для button_company_update
    # button_company_update = 'Изменить'
    # здесь нужно условие для button_folder_create
    # button_folder_create = 'Добавить'
    # здесь нужно условие для button_company_select
    comps = request.session["_auth_user_companies_id"]
    if len(comps) > 1:
        button_company_select = _("Сменить организацию")
    # if currentuser == current_company.author_id:
    #   button_company_create = 'Добавить'
    #   button_company_update = 'Изменить'
    #   button_folder_create = 'Добавить папку'
    # print(current_company.id)
    # foldertheme = Dict_Theme.objects.filter(is_active=True)
    # if current_folder == 0:
    #    themes_list = Folder.objects.filter(is_active=True, level=0).values('theme') #.distinct()
    # else:
    # themes_list = Folder.objects.filter(is_active=True, parent_id=current_folder).values('theme') #.distinct()
    # themes = Folder.objects.get(is_active=True, level=0) #.values('theme')
    # themes_list = themes.get_children().values('theme_id')  # .distinct()
    themes_list = folder_list.values("theme_id")
    foldertheme = Dict_Theme.objects.filter(id__in=themes_list)
    # types_list = Folder.objects.filter(is_active=True, parent_id=current_folder).values('type').distinct()
    types_list = folder_list.values("type_id")
    foldertype = Dict_FolderType.objects.filter(id__in=types_list)
    # print(themes_list)
    # print(foldertheme)
    if current_company.id in comps:
        button_folder_create = _("Добавить")
        button_folder_update = _("Изменить")
        button_file_create = _("Добавить")
    return render(
        request,
        template,
        {
            "nodes": folder_list.distinct(),  # .order_by(), # для удаления задвоений и восстановления иерархии
            "current_folder": current_folder,
            "root_folder_id": root_folder_id,
            "tree_folder_id": tree_folder_id,
            "current_company": current_company,
            "companyid": companyid,
            "user_companies": comps,
            "component_name": "files",
            "files": FolderFile.objects.filter(
                folder=current_folder, is_active=True
            ).select_related("author", "folder"),
            "objtype": "fldr",
            "obj_files_rights": obj_files_rights,
            "media_path": settings.MEDIA_URL,
            "button_company_select": button_company_select,
            # 'button_company_create': button_company_create,
            # 'button_company_update': button_company_update,
            "button_folder_create": button_folder_create,
            "button_folder_update": button_folder_update,
            "button_file_create": button_file_create,
            # 'button_folder_history': button_folder_history,
            # 'foldertheme': Dict_Theme.objects.filter(is_active=True),
            "foldertheme": foldertheme,
            "foldertheme_selectid": theme_selectid,
            "foldertype": foldertype,  # Dict_FolderType.objects.filter(is_active=True),
            "foldertype_selectid": type_selectid,
            "folder_myselectid": "-1",
            "object_list": "folder_list",
            "len_list": len_list,
        },
    )


class FolderCreate(AddFilesMixin, CreateView):
    model = Folder
    form_class = FolderForm
    # template_name = 'project_create.html'
    template_name = "object_form.html"

    # def get_success_url(self):
    #    print(self.object) # Prints the name of the submitted user
    #    print(self.object.id) # Prints None
    #    return reverse("webApp:project:stepTwo", args=(self.object.id,))

    def form_valid(self, form):
        form.instance.company_id = self.kwargs["companyid"]
        if self.kwargs["parentid"] != 0:
            form.instance.parent_id = self.kwargs["parentid"]
        form.instance.author_id = self.request.user.id
        self.object = form.save()  # Созадём новую папку
        af = self.add_files(
            form, "file", "folder"
        )  # добавляем файлы из формы (метод из AddFilesMixin)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = _("Новая Папка")
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # здесь нужно условие для 'action': 'create'
        kwargs.update(
            {
                "user": self.request.user,
                "action": "create",
                "companyid": self.kwargs["companyid"],
            }
        )
        return kwargs


class FolderUpdate(AddFilesMixin, UpdateView):
    model = Folder
    form_class = FolderForm
    # template_name = 'project_update.html'
    template_name = "object_form.html"

    def get_context_data(self, **kwargs):
        # context = super(ProjectUpdate, self).get_context_data(**kwargs)
        context = super().get_context_data(**kwargs)
        context["header"] = _("Изменить Папку")
        # kwargs = super(ProjectUpdate, self).get_form_kwargs()
        kwargs = super().get_form_kwargs()
        context["files"] = FolderFile.objects.filter(
            folder_id=self.kwargs["pk"], is_active=True
        ).order_by("uname")
        # print(context)
        # print(kwargs)
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # здесь нужно условие для 'action': 'update'
        kwargs.update({"user": self.request.user, "action": "update"})
        return kwargs

    def form_valid(self, form):
        self.object = form.save(
            commit=False
        )  # без commit=False происходит вызов save() Модели
        af = self.add_files(
            form, "file", "folder"
        )  # добавляем файлы из формы (метод из AddFilesMixin)
        ## Получаем старые значения для дальнейшей проверки на изменения
        # old = Folder.objects.filter(pk=self.object.pk).first()  # вместо objects.get(), чтоб не вызывало исключения при создании нового проекта
        # old_memb = old.members.values_list('id', 'username').all()
        # old_memb_count = old_memb.count()
        # old_memb_list = list(old_memb)
        self.object = form.save()
        return super().form_valid(form)


class UploadFiles(AddFilesMixin, FormView):
    form_class = UploadFilesForm
    template_name = "object_form.html"  # Replace with your template.
    # success_url = '/files/files_page0/' #reverse('my_file:folders0')  # Replace with your URL or reverse().
    # success_url = reverse_lazy("my_file:folders", kwargs={"companyid": "0", "pk": "0"})
    # success_url = reverse('views.folders')
    # success_url = reverse(folder_detail.html)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist("files")
        if form.is_valid():
            # for f in files:
            #    ...  # Do something with each file.
            # form.instance.author_id = self.request.user.id
            # self.object = form.save()  # Созадём новую папку
            self.pk = self.kwargs["pk"]
            self.object = Folder.objects.filter(id=self.pk).first()
            # print(self.object)
            af = self.add_files(
                form, "file", "folder"
            )  # добавляем файлы из формы (метод из AddFilesMixin)
            return super().form_valid(form)
        else:
            return super().form_invalid(form)

    def get_success_url(self):
        # print(self.pk)
        return reverse("my_file:folders", kwargs={"companyid": "0", "pk": self.pk})


@login_required  # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def folderfilter(request):
    # folderid = request.GET['folderid']
    companyid = request.GET["companyid"]
    themeid = request.GET["themeid"]
    typeid = request.GET["typeid"]
    my = request.GET["my"]
    currentuser = request.user.id
    # folder = Folder.objects.filter(id=folderid).first()
    # companyid = folder.company_id
    current_company = (
        Company.objects.filter(id=companyid)
        .select_related("author", "structure_type", "type", "currency")
        .first()
    )
    if companyid == 0:
        companyid = request.session["_auth_user_currentcompany_id"]
    # parent_folder = Folder.objects.filter(id=folderid).first()
    # folder_list = parent_folder.get_children()
    folder_list = Folder.objects.filter(is_active=True, company_id=companyid)
    # *** фильтруем по тематике ***
    if themeid != "-1":
        folder_list = folder_list.filter(theme_id=themeid)
    # *** фильтруем по типу ***
    if typeid != "-1":
        folder_list = folder_list.filter(type_id=typeid)
    # *** фильтр по принадлежности ***
    if my == "1":
        folder_list = folder_list.filter(author_id=currentuser)
    # **********
    # print(currentuser, my)
    nodes = folder_list.select_related(
        "author", "company", "theme", "type"
    ).distinct()  # .order_by()

    themes_list = folder_list.values("theme_id")
    foldertheme = Dict_Theme.objects.filter(id__in=themes_list)
    types_list = folder_list.values("type_id")
    foldertype = Dict_FolderType.objects.filter(id__in=types_list)
    # print(themes_list, foldertheme)

    object_message = ""
    if len(nodes) == 0:
        object_message = _("Папки не найдены!")

    return render(
        request,
        "folders_list.html",
        {
            "nodes": nodes,
            "current_company": current_company,
            "object_message": object_message,
            "foldertheme": foldertheme,
            "foldertype": foldertype,
            "myfolderselectid": my,
        },
    )


@login_required  # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def filefilter(request):
    folderid = request.GET["folderid"]
    sort = request.GET["sort"]
    sortdir = request.GET["sortdir"]
    my = request.GET["my"]
    currentuser = request.user.id
    if my == "-1":
        file_list = FolderFile.objects.filter(folder_id=folderid, is_active=True)
    elif my == "1":
        file_list = FolderFile.objects.filter(
            folder_id=folderid, is_active=True, author_id=currentuser
        )
    elif my == "2":
        file_list = FolderFile.objects.filter(
            folder_id=folderid, is_active=False, author_id=currentuser
        )
    file_list = file_list.select_related("author", "folder")
    # print(file_list)
    if sort == "1":
        if sortdir == "-1":
            file_list = file_list.order_by()
        elif sortdir == "1":
            file_list = file_list.order_by("uname")
        else:
            file_list = file_list.order_by("-uname")
    elif sort == "2":
        if sortdir == "-1":
            file_list = file_list.order_by()
        elif sortdir == "1":
            file_list = file_list.order_by("psize")
            print(file_list)
        else:
            file_list = file_list.order_by("-psize")
    elif sort == "3":
        if sortdir == "-1":
            file_list = file_list.order_by()
        elif sortdir == "1":
            file_list = file_list.order_by("datecreate")
        elif sortdir == "2":
            file_list = file_list.order_by("-datecreate")

    nodes = file_list.distinct()  # .order_by()

    obj_files_rights = 0
    current_folder = (
        Folder.objects.filter(id=folderid)
        .select_related("author", "company", "theme", "type")
        .first()
    )
    if currentuser == current_folder.author_id:
        obj_files_rights = 1

    object_message = ""
    if len(nodes) == 0:
        object_message = _("Файлы не найдены!")

    return render(
        request,
        "folderfile_list.html",
        {
            "files": nodes,
            "objtype": "fldr",
            "obj_files_rights": obj_files_rights,
            "object_message": object_message,
        },
    )
