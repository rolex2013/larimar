from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count, Min, Max, Sum, Avg

from django.views.generic import View, TemplateView, ListView, DetailView, CreateView
from django.views.generic.edit import UpdateView

from main.utils import AddFilesMixin #ObjectUpdateMixin

from main.models import Dict_Theme
from companies.models import Company

from files.models import Folder, FolderFile, Dict_FolderType

from .forms import FolderForm

@login_required   # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def folders(request, companyid=0, pk=0):

    if companyid == 0:
       companyid = request.session['_auth_user_currentcompany_id']

    request.session['_auth_user_currentcomponent'] = 'files'

    # *** фильтруем по тематике ***
    currentuser = request.user.id
    ftheme_selectid = 0
    #myprjstatus = 0 # для фильтра "Мои проекты"
    try:
       ftheme = request.POST['select_ftheme']
    except:
       folder_list = Folder.objects.filter(Q(author=request.user.id), is_active=True, company=companyid)
    else:
       if ftheme == "0":
          # если в выпадающем списке выбрано "Все активные"
          folder_list = Folder.objects.filter(Q(author=request.user.id), is_active=True, company=companyid)
       else:
          if ftheme == "-1":
             # если в выпадающем списке выбрано "Все"
             folder_list = Folder.objects.filter(Q(author=request.user.id), is_active=True, company=companyid)
          #elif ftheme == "-2":
          #   # если в выпадающем списке выбрано "Просроченные"
          #   project_list = Project.objects.filter(Q(author=request.user.id) | Q(assigner=request.user.id) | Q(members__in=[currentuser,]), is_active=True, company=companyid, dateclose__isnull=True, dateend__lt=datetime.datetime.now())
          else:
             folder_list = Folder.objects.filter(Q(author=request.user.id), is_active=True, company=companyid, theme=ftheme) #, dateclose__isnull=True)
       ftheme_selectid = ftheme
    #prjstatus_myselectid = myprjstatus
    # *******************************
    #project_list = project_list.order_by('dateclose')

    current_company = Company.objects.get(id=companyid)

    if pk == 0:
       current_folder = 0
       tree_folder_id = 0
       root_folder_id = 0
       #tree_project_id = 0
       template = "company_detail.html"
    else:
       current_folder = Folder.objects.filter(id=pk).first()
       #idpk = 'id=pk'
       #current_folder = Folder.objects.get({idpk})
       tree_folder_id = current_folder.tree_id
       root_folder_id = current_folder.get_root().id
       #tree_folder_id = current_folder.tree_id
       folder_list = current_folder.get_children()
       template = "folder_detail.html"

    len_list = len(folder_list)

    button_company_select = ''
    button_company_create = ''
    button_company_update = ''
    button_folder_create = ''
    button_folder_update = ''

    # здесь нужно условие для button_company_create
    # если текущий пользователь не является автором созданной текущей организации, то добавлять и изменять Компанию можно только в приложении Организации
    #button_company_create = 'Добавить'
    # здесь нужно условие для button_company_update
    #button_company_update = 'Изменить'
    # здесь нужно условие для button_folder_create
    #button_folder_create = 'Добавить'
    # здесь нужно условие для button_company_select
    comps = request.session['_auth_user_companies_id']
    if len(comps) > 1:
       button_company_select = 'Сменить организацию'
    #if currentuser == current_company.author_id:
    #   button_company_create = 'Добавить'
    #   button_company_update = 'Изменить'
    #   button_folder_create = 'Добавить папку'
    #print(current_company.id)
    if current_company.id in comps:
       button_folder_create = 'Добавить'
       button_folder_update = 'Изменить'
    return render(request, template, {
                              'nodes': folder_list.distinct(), #.order_by(), # для удаления задвоений и восстановления иерархии
                              'current_folder': current_folder,
                              'root_folder_id': root_folder_id,
                              'tree_folder_id': tree_folder_id,
                              'current_company': current_company,
                              'companyid': companyid,
                              'user_companies': comps,
                              'component_name': 'files',
                              'files': FolderFile.objects.filter(folder=current_folder, is_active=True),
                              'objtype': 'fldr',
                              'media_path': settings.MEDIA_URL,
                              'button_company_select': button_company_select,
                              #'button_company_create': button_company_create,
                              #'button_company_update': button_company_update,
                              'button_folder_create': button_folder_create,
                              'button_folder_update': button_folder_update,
                              #'button_folder_history': button_folder_history,
                              'foldertheme': Dict_Theme.objects.filter(is_active=True),
                              'ftheme_selectid': ftheme_selectid,
                              #'prjstatus_myselectid': prjstatus_myselectid,
                              'object_list': 'folder_list',
                              #'select_projectstatus': select_projectstatus,
                              'len_list': len_list,
                              #'fullpath': os.path.join(settings.MEDIA_ROOT, '///'),
                                                })


class FolderCreate(AddFilesMixin, CreateView):
    model = Folder
    form_class = FolderForm
    # template_name = 'project_create.html'
    template_name = 'object_form.html'

    # def get_success_url(self):
    #    print(self.object) # Prints the name of the submitted user
    #    print(self.object.id) # Prints None
    #    return reverse("webApp:project:stepTwo", args=(self.object.id,))

    def form_valid(self, form):
        form.instance.company_id = self.kwargs['companyid']
        if self.kwargs['parentid'] != 0:
            form.instance.parent_id = self.kwargs['parentid']
        form.instance.author_id = self.request.user.id
        self.object = form.save()  # Созадём новую папку
        af = self.add_files(form, 'file', 'folder')  # добавляем файлы из формы (метод из AddFilesMixin)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Новая Папка'
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # здесь нужно условие для 'action': 'create'
        kwargs.update({'user': self.request.user, 'action': 'create', 'companyid': self.kwargs['companyid']})
        return kwargs


class FolderUpdate(AddFilesMixin, UpdateView):
    model = Folder
    form_class = FolderForm
    # template_name = 'project_update.html'
    template_name = 'object_form.html'

    def get_context_data(self, **kwargs):
        # context = super(ProjectUpdate, self).get_context_data(**kwargs)
        context = super().get_context_data(**kwargs)
        context['header'] = 'Изменить Папку'
        # kwargs = super(ProjectUpdate, self).get_form_kwargs()
        kwargs = super().get_form_kwargs()
        context['files'] = FolderFile.objects.filter(folder_id=self.kwargs['pk'], is_active=True).order_by('uname')
        # print(context)
        # print(kwargs)
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # здесь нужно условие для 'action': 'update'
        kwargs.update({'user': self.request.user, 'action': 'update'})
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)  # без commit=False происходит вызов save() Модели
        af = self.add_files(form, 'file', 'folder')  # добавляем файлы из формы (метод из AddFilesMixin)
        ## Получаем старые значения для дальнейшей проверки на изменения
        #old = Folder.objects.filter(pk=self.object.pk).first()  # вместо objects.get(), чтоб не вызывало исключения при создании нового проекта
        #old_memb = old.members.values_list('id', 'username').all()
        #old_memb_count = old_memb.count()
        #old_memb_list = list(old_memb)
        self.object = form.save()
        return super().form_valid(form)