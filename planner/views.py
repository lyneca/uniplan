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
    '05 Mar': ['Lectures begin'],
    '30 Mar': ['Good Friday'],
    '31 Mar': ['Census date'],
    '02 Apr': ['Easter Monday', 'Mid-semester break begins'],
    '06 Apr': ['Mid-semester break ends'],
    '25 Apr': ['ANZAC Day'],
    '11 Jun': ['Queen\'s Birthday', 'Study vacation begins'],
    '15 Jun': ['Study vacation ends'],
    '18 Jun': ['Examination period begins'],
    '30 Jun': ['Examination period ends', 'Semester 1 ends'],
    '30 Jul': ['Lectures begin'],
    '31 Aug': ['Census date'],
    '24 Sep': ['Mid-semester break begins'],
    '28 Sep': ['Mid-semester break ends'],
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

class Week:
    def __init__(self, week):
        self.week_number = week
        self.tasks = []
        self.events = []

    def __str__(self):
        return "Week " + self.week_number

    def add_task(self, task):
        self.tasks.append(task)

    def add_event(self, event):
        self.events.append(event)

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
def get_days(request):
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
    if request.user.is_authenticated:
        units = request.user.profile.subjects.order_by('name')
        for unit in units:
            for task in unit.assessment_set.order_by('date'):
                delta = task.date - start_day
                if delta.days > 0:
                    weeks[math.floor(delta.days/7)][delta.days % 7].add_task(task)
    return weeks

def get_weeks(request):
    start_day = datetime(2018, 3, 5, tzinfo=UTC())  # This should be set to the first day of semester
    weeks = []
    for week_number in range(13):
        week = Week(week_number)
        for day in range(7):
            date = Day(start_day + timedelta(days=day, weeks=week_number))
            if date.date.strftime('%d %b') in dates:
                events = dates[date.date.strftime('%d %b')]
                for event in events:
                    week.add_event(event)
        weeks.append(week)
    if request.user.is_authenticated:
        units = request.user.profile.subjects.order_by('name')
        for unit in units:
            for task in unit.assessment_set.order_by('date'):
                delta = task.date - start_day
                if delta.days > 0:
                    weeks[math.floor(delta.days/7)].add_task(task)
    return weeks

def index(request):
    """
    Response Codes:
        0: success
        1: bad username/password
        2: passwords don't match
        3: username already exists
        4: invalid unit name
    """
    errors = {
        0: "SUCCESS!",
        1: "INVALID USERNAME OR PASSWORD",
        2: "PASSWORDS DO NOT MATCH",
        3: "USERNAME ALREADY EXISTS",
        4: "INVALID UNIT NAME"
    }
    if 'reason' in request.GET:
        reason = errors[int(request.GET['reason'])]
    else:
        reason = ''

    context = {
        'monthly_weeks': get_days(request),
        'weeks': get_weeks(request),
        'user': request.user,
        'units': Unit.objects.order_by('name'),
        'reason': reason,
    }
    return render(request, 'planner/index.html', context)

def generate_weekly(request):
    context = {
        'weeks': get_weeks(request)
    }
    return render(request, 'planner/weekly.html', context)

def generate_monthly(request):
    context = {
        'monthly_weeks': get_days(request)
    }
    return render(request, 'planner/monthly.html', context)

def auth_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        success = True
    else:
        success = False
        return redirect('/?reason=1')
    return redirect('/')

def auth_logout(request):
    logout(request)
    return redirect('/?reason=0')

def auth_register(request):
    username = request.POST['username']
    password = request.POST['password']
    password_2 = request.POST['password_2']
    if not password == password_2:
        return redirect('/?reason=2')

    if User.objects.filter(username=username).exists():
        return redirect('/?reason=3')

    user = User.objects.create_user(username, '', password)
    user.save()
    return redirect('/?reason=0')

def add_unit(request):
    subject = request.POST['unit']
    unit = Unit.objects.get(name=subject)
    if not unit:
        return redirect('/?reason=4')
    request.user.profile.subjects.add(unit)
    return redirect('/')

def remove_unit(request): 
    subject = request.POST['unit']
    unit = Unit.objects.get(name=subject)
    request.user.profile.subjects.remove(unit)
    return redirect('/')

def num_users(request):
    count = User.objects.all().count()
    return HttpResponse(str(count))

def num_units(request):
    count = Unit.objects.all().count()
    return HttpResponse(str(count))

def num_tasks(request):
    count = Assessment.objects.all().count()
    return HttpResponse(str(count))
