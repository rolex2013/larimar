from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Dict_Currency, CurrencyRate

# Create your views here.


@login_required   # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def finance(request):

    currencyrate_list = CurrencyRate.objects.filter(is_active=True)

    button_currencyrate_update = 'Обновить'

    return render(request, 'finance_detail.html', {
                                                       'button_currencyrate_update': button_currencyrate_update,
                                                       'currencyrate_list': currencyrate_list.distinct().order_by(),
                                                      })