# Generated by Django 4.2.3 on 2023-07-30 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('STUDENT', 'Elève'), ('TEACHER', 'Professeur'), ('SCHOOLADMIN', 'Administrateur Scolaire'), ('ADMIN', 'Administrateur')], max_length=50),
        ),
    ]