# Generated by Django 2.0 on 2017-12-12 06:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0003_assessment_unit'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assessment',
            old_name='time',
            new_name='date',
        ),
    ]
