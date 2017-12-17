from django.core.management.base import BaseCommand
from pprint import pprint
from bs4 import BeautifulSoup
import re
import requests
from planner.models import Unit, Assessment

def get_page(link):
    """
    this thing takes a link and shoves back some html
    """
    r = requests.get(link)
    r.raise_for_status()
    return r.content

def cusp(course_code):
    """
    NOTE: THERE IS NO WAY THIS FUNCTION SHOULD GET INTO PROD

    Takes a course code and returns a list containing dictionary objects which represent courses.
    All ye who enter, beware. There are list comprehensions abroad.
    """
    return [{'assessment_number': x[0], 'name': x[1], 'is_group': x[2], 'weight': x[3], 'due_string': x[4]} for x in [[x.text.strip() for x in x.find_all('td')][:-1] for x in BeautifulSoup(get_page('https://cusp.sydney.edu.au/students/view-unit-page/alpha/' + course_code), 'html.parser').find(string="Assessment Methods:").parent.next_element.next_element.next_element.next_element.next_element.find_all('tr')][1:]]

class Command(BaseCommand):
    def handle(self, *args, **options):
        units = open('units')
        for line in units:
            line = line.strip()
            name = line.split('|')[0]
            desc = line.split('|')[1]
            print(".. Inserting unit {}...".format(name))
            if Unit.objects.filter(name=name, long_name=desc).count() == 0:
                unit = Unit(name=name, long_name=desc)
                unit.save()
            else:
                unit = Unit.objects.get(name=name, long_name=desc)
            print("   Done.")
            try:
                tasks = cusp(name)
            except:
                print("   Unit page is weird, skipping")
                continue
            print(".. Found {} task{}.".format(len(tasks), 's' if len(tasks) == 1 else ''))
            print("   {} have distinct dates.".format(len([x for x in tasks if re.match(r"Week \d+", x['due_string'])])))
            for task in tasks:
                m = re.match(r"Week \d+", task['due_string'])
                e = re.match(r"Exam Period", task['due_string'])
                if m:
                    name = task['name']
                    week = int(m.group().split()[-1])
                    if Assessment.objects.filter(name=name, week=week, unit=unit).count() == 0:
                        print("    Adding {} on week {}".format(name, week))
                        a = Assessment(name=name, week=week, unit=unit)
                        a.save()
                    else:
                        print("    {} already exists, skipping".format(name, week))
                elif e:
                    name = task['name']
                    week = 14
                    print("    Adding {} to exam period".format(name, week))
                    if Assessment.objects.filter(name=name, week=week, unit=unit).count() == 0:
                        a = Assessment(name=name, week=week, unit=unit)
                        a.save()
                    else:
                        print("    {} already exists, skipping".format(name, week))
                else:
                    print("    Skipping {} - dunno when it is!".format(task['name']))
                    open("skips.txt", 'a').write(task['name'] + ': ' + task['due_string'] + '\n')
