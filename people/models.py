from django.conf import settings
from django.db import models

# Create your models here.
class People(models.Model):
    GENDER_CHOICES = (
        (1, 'masculin'),
        (0, 'féminin'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    gender = models.IntegerField(choices=GENDER_CHOICES, null=True, default=1)
    age = models.IntegerField(null=True, default=10)
    telephone = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    image = models.ImageField(blank=True, upload_to='profile')

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.firstname} {self.lastname}'


class SchoolAdmin(People):
    school = models.ForeignKey('school.School', on_delete=models.CASCADE, related_name='schooladmins')



    def __str__(self):
        return f'{self.firstname} {self.lastname}'


class WebAdmin(People):

    def __str__(self):
        return f'{self.firstname} {self.lastname}'


class Student(People):


    def fullname(self):
        return f'{self.firstname} {self.lastname}'



class Teacher(People):


    def __str__(self):
        return f'{self.firstname} {self.lastname}'


