from django.db import models

# Create your models here.

class Unit(models.Model):
    name = models.CharField(max_length=8)
    long_name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class User(models.Model):
    username = models.CharField(max_length=30)
    email = models.CharField(max_length=256)
    subjects = models.ManyToManyField(Unit)

    def __str__(self):
        return self.username

class Assessment(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField('date due/exam date')
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
