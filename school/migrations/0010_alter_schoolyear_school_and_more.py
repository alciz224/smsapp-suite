# Generated by Django 4.2.3 on 2023-09-14 21:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0003_teacher_subjects'),
        ('school', '0009_alter_timetable_classroom_alter_timetable_subject_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schoolyear',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='years', to='school.school'),
        ),
        migrations.AlterField(
            model_name='schoolyearteacher',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teachers', to='people.teacher'),
        ),
        migrations.AlterUniqueTogether(
            name='schoolyearstudent',
            unique_together={('student', 'level')},
        ),
        migrations.AlterUniqueTogether(
            name='schoolyearteacher',
            unique_together={('teacher', 'school_year')},
        ),
    ]
