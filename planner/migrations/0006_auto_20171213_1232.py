# Generated by Django 2.0 on 2017-12-13 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0005_auto_20171212_2142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='subjects',
            field=models.ManyToManyField(blank=True, to='planner.Unit'),
        ),
    ]
