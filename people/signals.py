from django.db.models.signals import post_save
from django.dispatch import receiver

from people.models import WebAdmin, Student, Teacher, SchoolAdmin
from user.models import CustomUser


@receiver(post_save, sender=CustomUser)
def user_profile_create(sender, instance, created, **kwargs):
    if created:
        user = instance
        if user.is_staff:

            admin_profile = WebAdmin.objects.create(user=user)
            admin_profile.save()
            print(user.user_type)

        elif user.user_type == 'STUDENT':
            student_profile= Student.objects.create(user=user)
            student_profile.firstname = user.first_name
            student_profile.lastname = user.last_name
            student_profile.save()
            print(user.user_type)

        elif user.user_type == 'TEACHER':

            teacher_profile = Teacher.objects.create(user=user)
            teacher_profile.firstname = user.first_name
            teacher_profile.lastname = user.last_name
            teacher_profile.save()
            print(user.user_type)

        elif user.user_type == 'SCHOOLADMIN':

            sa_profile = SchoolAdmin.objects.create(user=user)
            sa_profile.firstname = user.first_name
            sa_profile.lastname = user.last_name
            sa_profile.save()
            print(user.user_type)


