# Generated by Django 4.1 on 2022-12-01 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_usuario_departamento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cita',
            name='f_creacion_cita',
            field=models.DateField(auto_now_add=True, db_column='F_Creacion_Cita'),
        ),
        migrations.AlterField(
            model_name='cita',
            name='h_creacion_cita',
            field=models.TimeField(auto_now_add=True, db_column='H_Creacion_Cita'),
        ),
    ]
