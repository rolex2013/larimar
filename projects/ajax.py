from .models import Project, Task

def project_delete(request):
    if request.user.is_authenticated() and request.is_ajax() and request.POST:
       object_id = request.POST.get('id', None)
       b = get_object_or_404(Project, id=object_id)
       b.delete()
       data = {'message': 'delete'.format(b)}
       return HttpResponse(json.dumps(data), content_type='application/json')
    else:
       return JsonResponse({'error': 'Only authenticated users'}, status=404)

def project__filter(request, companyid=0):
    if request.user.is_authenticated() and request.is_ajax() and request.POST:
        if companyid == 0:
            companyid = request.session['_auth_user_currentcompany_id']
            # *** фильтруем по статусу ***
            prjstatus_selectid = 0
            try:
               prjstatus = request.POST['select_projectstatus']
            except:
               project_list = Project.objects.filter(is_active=True, company=companyid, dateclose__isnull=True)
            else:
               if prjstatus == "0":
                  # если в выпадающем списке выбрано "Все активные"
                  project_list = Project.objects.filter(is_active=True, company=companyid, dateclose__isnull=True)
               else:
                  if prjstatus == "-1":
                     # если в выпадающем списке выбрано "Все"
                     project_list = Project.objects.filter(is_active=True, company=companyid)
                  else:             
                     project_list = Project.objects.filter(is_active=True, company=companyid, status=prjstatus, dateclose__isnull=True)
            prjstatus_selectid = prjstatus
            nodes = project_list.order_by()
            # *******************************        
            return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return JsonResponse({'error': 'Only authenticated users'}, status=404)    