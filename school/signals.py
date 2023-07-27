from itertools import product

from django.db.models.signals import post_save
from django.dispatch import receiver

from school.models import SchoolYearStudent, Subject, MarkType, Mark


@receiver(post_save, sender=SchoolYearStudent)
def mark_student_handler(sender, instance, created, **kwargs):
    if created:
        stud = instance
        print('Student saved')

        subjects = Subject.objects.filter(classroom=instance.classroom_id)
        etype = MarkType.objects.filter(level=instance.level_id)
        list(subjects)
        list(etype)
        for sbj, ety in product(subjects, etype):
            marks = Mark(student=stud, subject=sbj, mark_type=ety)
            marks.save()



@receiver(post_save, sender = Subject)
def mark_subject_handler(sender, instance, created, **kwargs):
    if created:
        obj = instance
        print('Subject saved')
        students = SchoolYearStudent.objects.filter(classroom=obj.classroom_id)
        etype = MarkType.objects.filter(level=obj.classroom.level_id)
        for std, ety in product(students, etype):
            marks = Mark(student=std, subject=obj, mark_type=ety)
            marks.save()



@receiver(post_save, sender=MarkType)
def mark_mark_type_handler(sender, instance, created, **kwargs):
    if created:
        obj = instance
        print('mark-type saved')
        student_queryset = SchoolYearStudent.objects.filter(level=obj.level_id)
        subject_queryset = Subject.objects.filter(classroom__level_id=obj.level_id)

        joined_student_queryset = student_queryset.select_related('classroom')
        joined_subject_queryset = subject_queryset.select_related('classroom')
        product_list = list(product(joined_student_queryset, joined_subject_queryset))

        for item in product_list:
            student_instance = item[0]
            subject_instance = item[1]

            if student_instance.classroom_id == subject_instance.classroom_id:
                marks = Mark(student=student_instance,
                             subject=subject_instance,
                             mark_type=obj)
                marks.save()