import re

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.
from people.models import WebAdmin, SchoolAdmin, Teacher, Student


class CustomUserManager(BaseUserManager):

    def create_superuser(self, username, email, password):
        user= self.model(username=username, email=email)
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self.db)
        user.save()

    def create_admin_user(self, username, password):
        user = self.model(username=username, user_type='ADMIN')
        user.set_password(password)
        user.is_staff = True
        user.save(using=self.db)
        return user

    def create_school_admin_user(self, username, password, school):
        user = self.model(username=username, user_type='SCHOOLADMIN')
        user.set_password(password)
        user.school = school
        user.save(using=self.db)
        return user

    def create_teacher_user(self, username, password):
        user = self.model(username=username, user_type='TEACHER')
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_student_user(self, username, password):
        user = self.model(username=username, user_type='STUDENT')
        user.set_password(password)
        user.save(using=self.db)
        return user

class CustomUser(AbstractUser):
    USER_TYPES = (
        ('STUDENT', 'Elève'),
        ('TEACHER', 'Professeur'),
        ('SCHOOLADMIN', 'Administrateur Scolaire'),
        ('ADMIN', 'Administrateur')
    )
    school = models.ForeignKey('school.School', on_delete=models.CASCADE, null=True, blank=True)
    user_type = models.CharField(max_length=50, choices=USER_TYPES)



    objects = CustomUserManager()


    def __str__(self):
        return self.username

    """def get_profile(self):
        try:
            return self.people.webadmin
        except WebAdmin.DoesNotExist:
            try:
                return self.people.schooladmin
            except SchoolAdmin.DoesNotExist:
                try:
                    return self.people.teacher
                except Teacher.DoesNotExist:
                    try:
                        return self.people.student
                    except Student.DoesNotExist:
                        return None"""

