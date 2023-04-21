from django.utils import timezone
from datetime import date, datetime, timedelta


class SetColorMixin(object):
    model = None
    model_form = None
    template = None

    @property
    # цвет отображения, в зависимости от просроченности
    def color(self):

        colour = ''
        #print('===', self.name, type(self.dateend), isinstance(self.dateend, date), isinstance(self.dateend, datetime))
        if isinstance(self.dateend, datetime):
            date_end1 = timezone.now() + timedelta(days=3)
            date_end2 = timezone.now() + timedelta(days=10)
            if self.dateend < timezone.now():
                # все просроченные
                colour = 'red'
            elif self.dateend.day == timezone.now().day:
                # если срок исполнения истекает сегодня
                colour = 'magenta'
            elif self.dateend < date_end1:
                # если срок исполнения - ближайшие 3 дня
                colour = 'blue'
            elif self.dateend < date_end2:
                # если срок исполнения - ближайшие 10 дней
                colour = 'green'
        else:
            date_end1 = date.today() + timedelta(days=3)
            date_end2 = date.today() + timedelta(days=10)
            if self.dateend < date.today():
                colour = 'red'
            elif self.dateend == date.today():
                colour = 'magenta'
            elif self.dateend < date_end1:
                colour = 'blue'
            elif self.dateend < date_end2:
                colour = 'green'

        return colour
