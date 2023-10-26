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

    @property
    def fullname(self):
        return f'{self.firstname} {self.lastname}'



class Teacher(People):
    subjects = models.ManyToManyField('school.SubjectList', related_name='teachers')


    def __str__(self):
        return f'{self.firstname} {self.lastname}'

    @property
    def name_with_tile(self):
        if self.gender == 1:
            return f'M. {self.firstname} {self.lastname}'
        elif self.gender == 0:
            return f'Mme. {self.firstname} {self.lastname}'


