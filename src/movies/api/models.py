from django.db import models

# Create your models here.
class Director(models.Model):
    name = models.CharField(max_length=120)
    surname = models.CharField(max_length=120)  
    def __str__(self):
        return self.name + ' ' +self.surname
    
class Movie(models.Model):
    title = models.CharField(max_length=120)
    year = models.IntegerField(default=2020)
    director = models.ForeignKey(Director, on_delete=models.PROTECT, blank=True, null=True)
    def __str__(self):
        return self.title