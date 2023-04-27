from django.utils import timezone
from datetime import date, datetime, timedelta


class SetPropertiesDashboardMixin(object):
    model = None
    model_form = None
    template = None

    @property
    # цвет отображения, в зависимости от просроченности
    def color(self):

        colour = ''
        if str(self.object_name[0]) == 'fdb_tckt':
            date_end = self.datecreate
        else:
            date_end = self.dateend
        #print('===', self.name, type(self.dateend), isinstance(self.dateend, date), isinstance(self.dateend, datetime))
        if isinstance(date_end, datetime):
            date_end1 = timezone.now() + timedelta(days=3)
            date_end2 = timezone.now() + timedelta(days=10)
            if date_end < timezone.now():
                # все просроченные
                colour = 'red'
            elif date_end.day == timezone.now().day:
                # если срок исполнения истекает сегодня
                colour = 'magenta'
            elif date_end < date_end1:
                # если срок исполнения - ближайшие 3 дня
                colour = 'blue'
            elif date_end < date_end2:
                # если срок исполнения - ближайшие 10 дней
                colour = 'green'
        else:
            date_end1 = date.today() + timedelta(days=3)
            date_end2 = date.today() + timedelta(days=10)
            if date_end < date.today():
                colour = 'red'
            elif date_end == date.today():
                colour = 'magenta'
            elif date_end < date_end1:
                colour = 'blue'
            elif date_end < date_end2:
                colour = 'green'

        return colour

    @property
    def date_for_sort(self):
        if hasattr(self, 'dateend'):
            if isinstance(self.dateend, datetime):
                return self.dateend
            else:
                return datetime.combine(self.dateend, datetime.max.time()).astimezone(None)
        else:
            return self.datecreate
