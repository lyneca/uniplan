from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime, timedelta, tzinfo
import math
from .models import User, Unit, Assessment

ZERO = timedelta(0)

class UTC(tzinfo):
    def utcoffset(self, dt):
        return ZERO
    def tzname(self, dt):
        return "UTC"
    def dst(self, dt):
        return ZERO

class Day:
    def __init__(self, date):
        self.date = date
        self.tasks = []

    def __str__(self):
        return self.date.strftime('%D')

    def add_task(self, task):
        self.tasks.append(task)

# Create your views here.
def index(request):
    start_day = datetime(2018, 3, 5, tzinfo=UTC())  # This should be set to the first day of semester
    weeks = []
    for week in range(12):
        weeks.append([])
        for day in range(7):
            date = Day(start_day + timedelta(days=day, weeks=week))
            weeks[week].append(date)
    user = User.objects.order_by('id')[1]
    units = user.profile.subjects.order_by('name')
    for unit in units:
        for task in unit.assessment_set.order_by('date'):
            delta = task.date - start_day
            if delta.days > 0:
                weeks[math.floor(delta.days/7)][delta.days % 7].add_task(task)
            
    context = {
        'user': user,
        'units': {unit: unit.assessment_set.order_by('date') for unit in units},
        'weeks': weeks
    }
    return render(request, 'planner/index.html', context)
