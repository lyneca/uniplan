# Generated by Django 2.0 on 2017-12-14 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0002_auto_20171214_1438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessment',
            name='date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='date due/exam date'),
        ),
    ]
