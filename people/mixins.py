import decimal

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg, Sum, F, ExpressionWrapper, FloatField, DecimalField, IntegerField
from django.db.models.functions import Cast

from people.models import SchoolAdmin, WebAdmin, Teacher, Student
from school.models import SchoolYear, SchoolYearStudent, SchoolYearTeacher, Classroom, Mark


class UserInfoMixin(LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = {
            'username': self.request.user.username,
            'role': self.request.user.get_user_type_display()
        }
        if self.request.user.user_type == 'SCHOOLADMIN':
            profile = SchoolAdmin.objects.get(user=self.request.user)
            school = profile.school
            school_years = school.years
            school_year = self.request.session.get('school_year')
            context['profile'] = profile
            context['school'] = school
            context['school_years'] = school_years

            if school_year:
                context['school_year'] = school_year

        elif self.request.user.user_type == 'ADMIN':
            profile = WebAdmin.objects.get(user=self.request.user)
            context['profile'] = profile
        elif self.request.user.user_type == 'TEACHER':
            profile = Teacher.objects.get(user=self.request.user)
            school_years = SchoolYear.objects.filter(year__schoolyear__schoolyearteacher__teacher=profile)
            context['profile'] = profile
            context['school_years'] = school_years



        elif self.request.user.user_type == 'STUDENT':
            profile = Student.objects.get(user=self.request.user)
            school_years = SchoolYear.objects.filter(level__schoolyearstudent__student=profile)
            context['profile'] = profile
            context['school_years'] = school_years
            context['school_year'] = self.request.session.get('school_year')
            context['next'] = self.request.session.get('next')
            if context['school_year']:
                context['current_year_student'] = SchoolYearStudent.objects.get(level_id=int(context['school_year']),
                                                                                student=profile)
            print(list(context['school_years'].values_list('id', flat=True)))
        else:
            profile = None
            context['profile'] = profile
        return context

class StudentAverageMixin(UserInfoMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = context.get('current_year_student')
        classroom = Classroom.objects.get(id=student.classroom.id)

        subjects = classroom.subjects.all()
        coef_count = subjects.aggregate(
            coef_sum=Sum('coef')
        )
        context['classroom'] = classroom

        def get_student_avg(student):
            student_marks = Mark.objects.filter(student=student)
            subject_count = student.classroom.subjects.count()

            avg_mark = student_marks.values('mark_type__name').annotate(
                avg_mark1=ExpressionWrapper(Sum(F('mark1')) / subject_count,
                                            output_field=FloatField()),
                avg_mark2=ExpressionWrapper(Sum(F('mark2') * F('subject__coef')) / coef_count['coef_sum'],
                                            output_field=FloatField()),
                avg_gen=ExpressionWrapper((F('avg_mark1') + F('avg_mark2')) / 2,
                                            output_field=FloatField())
            ).order_by('mark_type')
            return avg_mark
        avg_mark = get_student_avg(student)
        print(avg_mark)
        context['avg_mark'] = avg_mark

        def get_student_subject_avg(student, marktype):
            student_marks = Mark.objects.filter(student=student, mark_type=marktype)
            print('string: ', student_marks.query)
            student_marks_avg = student_marks.values('subject__name__name__name', 'subject__coef', 'mark1', 'mark2').annotate(
                points=ExpressionWrapper((F('mark1') + F('mark2')), output_field=FloatField()),
                avg_mark=ExpressionWrapper((F('mark1')+F('mark2'))/2, output_field=FloatField())
            )
            print('string 2: ', student_marks_avg.query)
            return student_marks_avg

        marktypes = student.level.marktypes.all()
        subject_mark_dict = {}
        for mt in marktypes:
            sm = get_student_subject_avg(student, mt)
            subject_mark_dict[mt.name] = sm

        print('this one', subject_mark_dict)
        context['student_subject_avg'] = subject_mark_dict
        return context

class TeacherClassroomAverageMixin(UserInfoMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Teacher.objects.get(user=self.request.user)
        school_year = self.request.session.get('school_year')
        if school_year:
            context['school_year'] = school_year
            current_teacher = SchoolYearTeacher.objects.get(teacher=profile, school_year=school_year)
            current_teacher_subjects = current_teacher.subjects.all().select_related('level')

            def get_student_avg_by_classroom(subject):
                mark_types = subject.level.marktypes.all()
                sub_mark_per_marktype = []
                for i in mark_types:
                    x = i
                    mt_name = x.name
                    student_marks = Mark.objects.filter(subject=subject, mark_type=x).values(
                        'student__student__firstname',
                        'student__student__lastname',
                        'mark1',
                        'mark2')
                    obj = {'mark_type': mt_name, 'marks': student_marks}
                    sub_mark_per_marktype.append(obj)
                return sub_mark_per_marktype

            context['school_year_teacher'] = current_teacher_subjects
            context['current_teacher_subjects'] = current_teacher_subjects
            # print('teacher: ', current_teacher)
            # print('teacher_subjects: ', current_teacher_subjects)
            current_teacher_subject_mark_list = []
            for subject in context['current_teacher_subjects']:
                subject_name = subject.name.name.name
                classroom = subject.classroom
                marks = get_student_avg_by_classroom(subject)
                obj = {'classroom': classroom,
                       'subject': subject_name,
                       'marks': marks}
                current_teacher_subject_mark_list.append(obj)

            teacher_subject_mark_list = current_teacher_subject_mark_list
            for i in teacher_subject_mark_list:
                print('------------------------------')
                print('teacher_subject_classroom: ', i['classroom'])
                print('teacher_subject_subject: ', i['subject'])
                print('teacher_subject_marks: ', i['marks'])
                for z in i['marks']:
                    print('z: ', z['mark_type'])

            context['teacher_subject_mark_list'] = teacher_subject_mark_list
        return context








