from django.http import HttpResponse
from django.shortcuts import render, redirect
from datetime import datetime, timedelta, tzinfo
from django.contrib.auth import authenticate, login, logout
import math
from .models import User, Unit, Assessment

dates = {
    '01 Jan': ['New Year\'s Day'],
    '26 Jan': ['Australia Day'],
    '26 Feb': ['Orientation Week (26 February - 2 March)'],
    '05 Mar': ['Lectures begin (Semester 1)'],
    '30 Mar': ['Good Friday'],
    '31 Mar': ['Census date (Semester 1)'],
    '02 Apr': ['Easter Monday', 'Mid-semester break begins (Semester 1)'],
    '06 Apr': ['Mid-semester break ends (Semester 1)'],
    '25 Apr': ['ANZAC Day'],
    '11 Jun': ['Queen\'s Birthday', 'Study vacation begins (Semester 1)'],
    '15 Jun': ['Study vacation ends (Semester 1)'],
    '18 Jun': ['Examination period begins'],
    '30 Jun': ['Examination period ends', 'Semester 1 ends'],
    '30 Jul': ['Lectures begin (Semester 2)'],
    '31 Aug': ['Census date (Semester 2)'],
    '24 Sep': ['Mid-semester break begins (Semester 2)'],
    '28 Sep': ['Mid-semester break ends (Semester 2)'],
    '01 Oct': ['Labour Day'],
    '05 Nov': ['Study vacation begins'],
    '09 Nov': ['Study vacation ends'],
    '12 Nov': ['Examination period begins'],
    '24 Nov': ['Examination period ends', 'Semester 2 ends'],
    '25 Dec': ['Christmas Day'],
    '26 Dec': ['Boxing Day']
}

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
        self.events = []

    def __str__(self):
        return self.date.strftime('%D')

    def add_task(self, task):
        self.tasks.append(task)

    def add_event(self, event):
        self.events.append(event)

# Create your views here.
def index(request):
    start_day = datetime(2018, 3, 5, tzinfo=UTC())  # This should be set to the first day of semester
    weeks = []
    for week in range(13):
        weeks.append([])
        for day in range(7):
            date = Day(start_day + timedelta(days=day, weeks=week))
            if date.date.strftime('%d %b') in dates:
                events = dates[date.date.strftime('%d %b')]
                for event in events:
                    date.add_event(event)
            weeks[week].append(date)
    print(request.user.is_authenticated)
    print(request.user.username)
    if request.user.is_authenticated:
        units = request.user.profile.subjects.order_by('name')
        for unit in units:
            for task in unit.assessment_set.order_by('date'):
                delta = task.date - start_day
                if delta.days > 0:
                    weeks[math.floor(delta.days/7)][delta.days % 7].add_task(task)
            
    context = {
        'user': request.user,
        'units': Unit.objects.order_by('name'),
        'weeks': weeks
    }
    return render(request, 'planner/index.html', context)

def auth_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        success = True
    else:
        success = False
    return redirect('/')

def auth_logout(request):
    logout(request)
    return redirect('/')
