# Generated by Django 4.1 on 2022-12-02 21:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_alter_cita_client_solicita_cita'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cita',
            name='secre_asigna_cita',
            field=models.ForeignKey(blank=True, db_column='Secre_Asigna_Cita', limit_choices_to={'tipo_usuario': 'ES'}, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='secre_cita', to=settings.AUTH_USER_MODEL, verbose_name='Secretaria a cargo'),
        ),
    ]