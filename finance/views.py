from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
#from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, HttpResponseNotFound, JsonResponse
import requests
#from lxml import etree as et
from datetime import datetime
from dateutil.parser import *

from .models import Dict_Currency, CurrencyRate

# Create your views here.


@login_required   # декоратор для перенаправления неавторизованного пользователя на страницу авторизации
def finance(request):

    r_rate = ''
    r_base = ''
    r_date = ''  
    #r = requests.get('https://api.exchangeratesapi.io/latest?start_at=2020-05-27&end_at=2020-05-28&symbols=USD,GBP,RUB,EUR').json()
    #r_error = r['error']
    #if r_error == '':
    #   r_rate = r['rates']
    #   r_base = r['base']
    #   r_date = r['date']        
       #print(rate['rates'])

    r = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json() 
    # можно доставать курсы по дате:
    #r = requests.get('https://www.cbr-xml-daily.ru/archive/2020/05/29/daily_json.js').json() 

    # на всякий случай загружаем курсы на предыдущую дату
    r_date = r['PreviousDate']
    r_date = parse(r_date)
    r_base = 'RUB'   
    r_curr = r['Valute']
    currents_list = Dict_Currency.objects.filter(is_active=True)    
    for curr in currents_list:
        if curr.code_char == 'RUB':
           r_value = 1            
        else:
           r_data = r_curr[curr.code_char]
           r_value = r_data['Previous']            
        cr = CurrencyRate(currency_id=curr.id, date=r_date, rate=r_value)
        try: 
           cr.save()
        except IntegrityError:
           print('Курс на предыдущую дату уже загружен в БД!') 

    # загружаем курсы на текущую дату
    r_date = r['Date']
    #r_date = r_date[0:10] + ' ' + '0' + str(int(r_date[11:13]) - int(r_date[19:22])) + r_date[13:19]
    #r_date = datetime.strptime(r_date, '%y-%m-%dT%H:%M:%S')
    #r_date = datetime.datetime.strptime(r_date, '%d.%m.%Y %H:%M:%S')
    r_date = parse(r_date)
    r_base = 'RUB'   
    r_curr = r['Valute']
    currents_list = Dict_Currency.objects.filter(is_active=True) #.exclude(code_char='RUB')    
    for curr in currents_list:
        if curr.code_char == 'RUB':
           r_value = 1            
        else:
           r_data = r_curr[curr.code_char]
           r_value = r_data['Value']            
        cr = CurrencyRate(currency_id=curr.id, date=r_date, rate=r_value)
        try: 
           cr.save()
        except IntegrityError:
        #print(curr.id)
           print('Курс на текущую дату уже загружен в БД!')
        #print(r_value)
        #print(r_date[11:13])
        #print(r_date[19:22])     
        #print(r_date[13:19])           
        #2020-05-30T11:30:00+03:00

    #r1 = requests.get('http://www.cbr.ru/scripts/XML_daily.asp?date_req=29/05/2020')
    ##root = et.XML(r1.text)
    ##root = et.Element('ValCurs')
    ##print(et.ValCurs)
    ##r1.encoding = 'utf-8'
    #print(r1.encoding)
    #print(r1.text)
    #print(r)

    currencyrate_list = CurrencyRate.objects.filter(is_active=True)    

    button_currencyrate_update = 'Обновить'

    return render(request, 'finance_detail.html', {
                                                       'button_currencyrate_update': button_currencyrate_update,
                                                       'currencyrate_list': currencyrate_list.distinct().order_by(),
                                                       #'r_error': r_error,
                                                       'r_rate': r_rate,
                                                       'r_base': r_base,
                                                       'r_date': r_date,
                                                       #'r_xml': r1.text,
                                                  }
                 )