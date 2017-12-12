from django.http import HttpResponse
from django.shortcuts import render
from .models import User, Unit, Assessment

# Create your views here.
def index(request):
    user = User.objects.order_by('id')[0]
    units = user.subjects.order_by('name')
    context = {
        'user': user,
        'units': {unit: unit.assessment_set.order_by('name') for unit in units}
    }
    return render(request, 'planner/index.html', context)
