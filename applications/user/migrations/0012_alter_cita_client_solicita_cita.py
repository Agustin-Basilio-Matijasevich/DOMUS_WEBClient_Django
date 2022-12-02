# Generated by Django 4.1 on 2022-12-02 18:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_alter_cita_ai_atiende_cita_alter_usuario_apellidos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cita',
            name='client_solicita_cita',
            field=models.ForeignKey(db_column='Client_Solicita_Cita', limit_choices_to=models.Q(('tipo_usuario', 'CP'), ('tipo_usuario', 'CC'), _connector='OR'), on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL, verbose_name='Cliente quien solicita'),
        ),
    ]
