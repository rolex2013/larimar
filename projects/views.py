from django.http import HttpResponse

def home_project_view(request):
    return HttpResponse('<h1>Добрый день!</h1>')
