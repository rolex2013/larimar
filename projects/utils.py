from .models import Project, Task, TaskComment

from django.shortcuts import render, redirect, get_object_or_404

class ObjectUpdateMixin:
    model = None
    model_form = None
    template = None

    def get(self, request, pk):
        obj = self.model.objects.get(id=pk)
        bound_form = self.model_form(instance=obj)
        return render(request, self.template, context={'form': bound_form, self.model.__name__.lower(): obj})

    def post(self, request, pk):
        obj = self.model.objects.get(id=pk)
        bound_form = self.model_form(request.POST, instance=obj)    
        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)
        return render(request, self.template, context={'form': bound_form, self.model.__name__.lower(): obj})        