from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.
from django.db.models import Max

from people.models import Student, Teacher
from user.models import CustomUser

"""SCHOOL MODEL"""
class School(models.Model):

    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100, default=None)
    phone = models.CharField(max_length=100, default=None)
    email = models.EmailField(blank=True, null=True, default=None)

    def __str__(self):
        return self.name

class Year(models.Model):
    start_year = models.PositiveIntegerField(unique=True)
    end_year = models.PositiveIntegerField(unique=True)

    class Meta:
        unique_together = ['start_year', 'end_year']

    def clean(self):
        if self.start_year >= self.end_year:
            raise ValidationError("l'année du debut doit etre inférieur à celle de la fin! ")
        if self.start_year +1 != self.end_year:
            raise ValidationError("L'interval entre le debut et la fin doit etre une année")





    def __str__(self):
        return f'{self.start_year} - {self.end_year}'

class SchoolYear(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ['school', 'year']

    def __str__(self):
        return f'{self.school}-{self.year}'

class LevelChoice(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_high_school = models.BooleanField()

    def __str__(self):
        return self.name

class Level(models.Model):
    name = models.ForeignKey(LevelChoice, on_delete=models.CASCADE)
    school_year = models.ForeignKey(SchoolYear, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['name', 'school_year']

    def __str__(self):
        return f'{self.name}'

class SubjectList(models.Model):

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class SubjectChoice(models.Model):

    name = models.ForeignKey(SubjectList, on_delete=models.CASCADE)
    level = models.ForeignKey(LevelChoice, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['name', 'level']

    def __str__(self):
        return self.name.name


class ClassroomList(models.Model):

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class ClassroomChoice(models.Model):

    name = models.ForeignKey(ClassroomList, on_delete=models.CASCADE)
    level = models.ForeignKey(LevelChoice, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['name', 'level']

    def __str__(self):
        if self.level.is_high_school:
            return f'{self.name.name} {self.level}'
        else:
            return f'{self.name.name} Annéé'


class Classroom(models.Model):

    name = models.ForeignKey(ClassroomChoice, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    section = models.IntegerField(default=0, null=True)

    def clean(self):
        super().clean()

        if self.name.level != self.level.name:
            raise ValidationError("Le nom selectionné pour cette classe n'est pas approprié!")

    def save(self, *args, **kwargs):
        self.clean()
        name = self.name
        level = self.level
        maxval = Classroom.objects.filter(name=name, level=level).aggregate(maxi=Max('section'))
        if maxval['maxi']==None:
            self.section = 1
            return super(Classroom, self).save(*args, **kwargs)
        else:
            self.section = maxval['maxi'] + 1
            return super(Classroom, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name.__str__()} {self.section}'

    def get_student_count(self):
        return self.schoolyearstudent_set.count()

    def get_male_count(self):
        return self.schoolyearstudent_set.filter(student__gender=1).count()

    def get_female_count(self):
        return self.schoolyearstudent_set.filter(student__gender=0).count()








class SchoolYearStudent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='studentsystudents')
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    has_promotion = models.BooleanField()

    def __str__(self):
        return self.student.firstname


class SchoolYearTeacher(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    school_year = models.ForeignKey(SchoolYear, on_delete=models.CASCADE)
    subject_taught = models.ManyToManyField(SubjectList)



    def __str__(self):
        return self.teacher.__str__()

class Subject(models.Model):

    name = models.ForeignKey(SubjectChoice, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    coef = models.IntegerField(null=False, default=1)
    teacher = models.ForeignKey(SchoolYearTeacher, on_delete=models.SET_NULL, null=True, blank=True, editable=True,
                                related_name='teachersubjects')

    class Meta:
        unique_together = ['name', 'classroom']



    def __str__(self):
        return self.name.name.name
    @property
    def getname(self):
        return self.name.name.name

    def clean(self):
        if self.name.level.name != self.classroom.name.level.name:
            raise ValidationError('cette matière ne correspond pas à la classe selectionnée!')




class MarkType(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='levelmarks')
    name = models.CharField(max_length=50)
    max_mark = models.DecimalField(max_digits=5, decimal_places=2, default=20)
    is_active = models.BooleanField(default=False)
    is_released = models.BooleanField(default=False)

    class Meta:
        unique_together = ['level', 'name']


    def __str__(self):
        return self.name

class Mark(models.Model):
    student = models.ForeignKey(SchoolYearStudent, on_delete=models.CASCADE, related_name='studentmarks')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='subjectmarks')
    mark_type = models.ForeignKey(MarkType, on_delete=models.CASCADE, related_name='marktypemarks')

    mark1 = models.DecimalField(max_digits=4,
                                decimal_places=2,
                                null=True,
                                blank=True,
                                validators=[MinValueValidator(0), MaxValueValidator(20)])
    mark2 = models.DecimalField(max_digits=4,
                                decimal_places=2,
                                null=True,
                                blank=True,
                                validators=[MinValueValidator(0), MaxValueValidator(20)])
    updated_by = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True, related_name='updatedmarks')

    class Meta:
        unique_together = ['student', 'subject', 'mark_type']
        ordering = ['student']

    def clean(self):
        super().clean()
        if self.mark1 is not None or self.mark2 is not None:
            if self.mark1 > self.mark_type.max_mark or self.mark2 >self.mark_type.max_mark:
                raise ValidationError(f"La note saisie est supérieure à {self.mark_type.max_mark}. Veuillez saisir une note dans l'interval de 0 à {self.mark_type.max_mark} !")
            if self.mark1 < 0 or self.mark2 < 0:
                raise ValidationError(f"La note saisie est inférieure à 0. Veuillez saisir une note dans l'interval de 0 à {self.mark_type.max_mark} !")


    def mark1_d(self):
        if self.mark1:
            if self.mark1 % 1 == 0:
                return f'{self.mark1:.0f}'
            else:
                return f'{self.mark1:.2f}'
        else:
            return self.mark1

    def mark2_d(self):
        if self.mark2:
            if self.mark2 % 1 == 0:
                return f'{self.mark2:.0f}'
            else:
                return f'{self.mark2:.2f}'
        else:
            return self.mark2

    def __str__(self):
        return f'{self.student}-{self.subject}-{self.mark_type}'


class SchoolInfo(models.Model):
    school_year = models.ForeignKey(SchoolYear, on_delete=models.CASCADE, related_name='schoolyearinfos')
    title = models.CharField(max_length=100, blank=False, null=False, help_text="titre de l'information")
    content = models.TextField(help_text="contenu de l'information")
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    to_all = models.BooleanField()
    to_level = models.ManyToManyField(Level, related_name='levelinfos')
    to_classroom = models.ManyToManyField(Classroom, related_name='classroominfos')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)


class MonthlySchedule(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False, help_text="le nom peut etre mensuel, trimestriel ou semestriel. Ex: ('Janvier', '1er trimestre')")
    school = models.ForeignKey(SchoolYear, on_delete=models.CASCADE)
    is_current = models.BooleanField(help_text="en l'activant, il devient l'emploi du temps courant que les professeurs et élèves vérons dans leur interface")
    class Meta:
        unique_together = ['name', 'school']

    def __str__(self):
        return self.name


class TimeTable(models.Model):
    DAYS = (
        ('LUNDI', 'Lundi'),
        ('MARDI', 'Mardi'),
        ('MERCREDI', 'Mercrédi'),
        ('JEUDI', 'Jeudi'),
        ('VENDREDI', 'Vendredi'),
        ('SAMEDI', 'Samedi'),
        ('DIMANCHE', 'Dimanche'),
    )
    schedule = models.ForeignKey(MonthlySchedule, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    day = models.CharField(max_length=50, choices=DAYS, null=False, blank=False)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='timetables', editable=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='timetables')

    def __str__(self):
        return f'{self.schedule}-{self.day}-{self.start_time}-{self.end_time}-{self.classroom}'
    @property
    def taught_by(self):
        if self.subject.teacher:
            return self.subject.teacher.teacher.name_with_tile
        else:
            return '-'










