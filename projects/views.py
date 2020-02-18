from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, TemplateView, ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView

from .models import Project, Task, TaskComment
from .forms import ProjectForm, TaskForm, TaskcommentForm
from .utils import ObjectUpdateMixin

class ProjectsHome(TemplateView):
   template_name = 'home.html'

class ProjectsList(ListView):
    model = Project
    template_name = 'projects.html' 

class ProjectDetail(DetailView):
    model = Project
    template_name = 'project_detail.html'   

#class ProjectsEditView(DetailView):
#    model = Project
#    template_name = 'project_edit.html' 

#class TasksListView(ListView):
#    model = Task
#    template_name = 'task.html' #'tasks.html' 
    #def get_queryset(self):
    #    return Task.objects.filter(Task.name!='war')[:5] # Получить 5 книг, содержащих 'war' в заголовке

class TaskDetail(DetailView):
    model = Task
    template_name = 'task_detail.html'  

#class CommentsListView(ListView):
#   model = TaskComment
#    template_name = 'taskcomments.html' 

class CommentDetail(DetailView):
    model = TaskComment
    template_name = 'taskcomment_detail.html'


def project_add(request):
    if request.method == "POST":
        form = ProjectForm(request.POST or None)
        if form.is_valid():
            new_project = form.save(commit=False)
            new_project.author = request.user
            form.save()
            return redirect('my_project:project_detail', pk=new_project.pk)
    else:
        form = ProjectForm()
    return render(request, 'project_add.html', {'form': form})

class ProjectUpdate(UpdateView):    
    model = Project
    form_class = ProjectForm
    #fields = ['name', 'description', 'assigner', 'datebegin', 'dateend']
    template_name = 'project_update.html'
    

class Project_Update(ObjectUpdateMixin, View):    
    model = Project
    model_form = ProjectForm
    template = 'project_update.html'


     
def project_delete(request, pk):
#    try:
#        project = Project.objects.get(id=id)
#        project.delete()
#        return HttpResponseRedirect("/")
#    except Project.DoesNotExist:
        return HttpResponseNotFound("<h2>Проект не найден!</h2>")


def task_add(request, projectid):
    if request.method == "POST":
        form = TaskForm(request.POST or None)
        if form.is_valid():
            new_task = form.save(commit=False)     
            new_task.project = Project(projectid)
            new_task.author = request.user
            form.save()
            return redirect('my_project:task_detail', pk=new_task.pk)
    else:
        form = TaskForm()
    return render(request, 'task_add.html', {'form': form, 'projectid': projectid})

def taskcomment_add(request, taskid):
    if request.method == "POST":
        form = TaskcommentForm(request.POST or None)
        if form.is_valid():
            new_taskcomment = form.save(commit=False)
            new_taskcomment.task = Task(taskid)
            new_taskcomment.author = request.user
            form.save()
            #return redirect('my_project:taskcomment_detail', pk=new_taskcomment.pk)
            return redirect('my_project:task_detail', pk=taskid)
    else:
        form = TaskcommentForm()
    return render(request, 'taskcomment_add.html', {'form': form, 'taskid': taskid})

#def Contacts(request):   
#        return HttpResponse('Contact form')