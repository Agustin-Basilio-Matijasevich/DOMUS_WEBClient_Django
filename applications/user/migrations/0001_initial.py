# Generated by Django 3.2.12 on 2022-12-03 05:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=20, unique=True)),
                ('dni_cuil', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=50, null=True)),
                ('nombres', models.CharField(max_length=50)),
                ('apellidos', models.CharField(max_length=50, null=True)),
                ('sexo', models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino'), ('NE', 'No Especifica')], default='NE', max_length=10)),
                ('salario_mensual', models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True)),
                ('departamento', models.CharField(blank=True, choices=[('COM', 'Comercializacion'), ('ADM', 'Administracion')], max_length=16, null=True)),
                ('foto_perfil', models.TextField(blank=True, null=True)),
                ('tipo_usuario', models.CharField(choices=[('ES', 'Empleado_Secretario'), ('EAI', 'Empleado_Agente Inmobiliario'), ('EM', 'Empleado_Marketing'), ('EJD', 'Empleado_Jefe de Departamento'), ('EC', 'Empleado_Cajero'), ('EAS', 'Empleado_Administrador de Sistema'), ('EGG', 'Empleado_Gerente General'), ('CP', 'Cliente_Particular'), ('CC', 'Cliente_Corporativo')], max_length=10)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name_plural': 'Listado de Usuarios',
                'db_table': 'usuario',
            },
        ),
        migrations.CreateModel(
            name='Caja',
            fields=[
                ('id_caja', models.AutoField(db_column='ID_Caja', primary_key=True, serialize=False)),
                ('descripcion_caja', models.CharField(db_column='Descripcion_Caja', max_length=100)),
                ('isopen', models.BooleanField(db_column='IsOpen', default=False)),
            ],
            options={
                'db_table': 'caja',
            },
        ),
        migrations.CreateModel(
            name='Ciudad',
            fields=[
                ('id_ciudad', models.AutoField(db_column='ID_Ciudad', primary_key=True, serialize=False)),
                ('nombre_ciudad', models.CharField(db_column='Nombre_Ciudad', max_length=20)),
            ],
            options={
                'verbose_name_plural': 'Ciudades',
                'db_table': 'ciudad',
            },
        ),
        migrations.CreateModel(
            name='ContratoCerrado',
            fields=[
                ('nro_contrato', models.AutoField(db_column='NRO_Contrato', primary_key=True, serialize=False)),
                ('f_creacion_contrato', models.DateField(db_column='F_Creacion_Contrato')),
                ('f_caduca_contrato', models.DateField(blank=True, db_column='F_Caduca_Contrato', null=True)),
                ('monto', models.DecimalField(db_column='Monto', decimal_places=0, max_digits=10)),
                ('tipo_contrato', models.CharField(choices=[('VEN', 'Venta'), ('ALQ', 'Alquiler')], db_column='Tipo_Contrato', max_length=8)),
                ('ai_responsable_contrato', models.ForeignKey(db_column='AI_Responsable_Contrato', on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
                ('client_involucrado_contrato', models.ForeignKey(db_column='Client_Involucrado_Contrato', on_delete=django.db.models.deletion.RESTRICT, related_name='client_contrato', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'contrato_cerrado',
            },
        ),
        migrations.CreateModel(
            name='Idioma',
            fields=[
                ('nombre_idioma', models.CharField(db_column='Nombre_Idioma', max_length=20, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'idioma',
            },
        ),
        migrations.CreateModel(
            name='Pais',
            fields=[
                ('nombre_pais', models.CharField(db_column='Nombre_Pais', max_length=20, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name_plural': 'Paises',
                'db_table': 'pais',
            },
        ),
        migrations.CreateModel(
            name='Propiedad',
            fields=[
                ('id_propiedad', models.AutoField(db_column='ID_Propiedad', primary_key=True, serialize=False, verbose_name='Codigo Propiedad')),
                ('tipo_propiedad', models.CharField(choices=[('CAS', 'Casa'), ('DEP', 'Departamento'), ('GAL', 'Galpon'), ('CAMP', 'Campo'), ('TER', 'Terreno')], db_column='Tipo_Propiedad', max_length=12, verbose_name='Propiedad de tipo')),
                ('pisos', models.PositiveIntegerField(db_column='Pisos', verbose_name='Piso')),
                ('metros_cuadrados', models.DecimalField(db_column='Metros_Cuadrados', decimal_places=0, max_digits=10, verbose_name='Metros Cuadrados')),
                ('direccion', models.CharField(db_column='Direccion', max_length=100, verbose_name='Direccion')),
                ('estado_propiedad', models.CharField(choices=[('VEN', 'Venta'), ('ALQ', 'Alquiler')], db_column='Estado_Propiedad', max_length=8, verbose_name='Estado de la Propiedad')),
                ('precio_sugerido', models.DecimalField(db_column='Precio_Sugerido', decimal_places=0, max_digits=10, verbose_name='Precio sugerido')),
                ('id_adquiere_o_alquila', models.ForeignKey(blank=True, db_column='ID_Adquiere_o_Alquila', null=True, on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
                ('id_ciudad_propiedad', models.ForeignKey(db_column='ID_Ciudad_Propiedad', on_delete=django.db.models.deletion.RESTRICT, to='user.ciudad', verbose_name='Ciudad donde se encuentra')),
                ('id_dueño', models.ForeignKey(db_column='ID_Dueño', on_delete=django.db.models.deletion.RESTRICT, related_name='dueño_propiedad', to=settings.AUTH_USER_MODEL, verbose_name='Dueño a cargo')),
            ],
            options={
                'verbose_name_plural': 'Lista de Propiedades',
                'db_table': 'propiedad',
            },
        ),
        migrations.CreateModel(
            name='RegistroDeCitas',
            fields=[
                ('id_registro', models.AutoField(db_column='ID_Registro', primary_key=True, serialize=False)),
                ('nro_cita', models.PositiveIntegerField(db_column='NRO_Cita')),
                ('fechas_field', models.CharField(db_column='Fechas=>', max_length=8)),
                ('fh_creacion', models.DateTimeField(db_column='FH_Creacion')),
                ('fh_asignacion', models.DateTimeField(db_column='FH_Asignacion')),
                ('fh_cita', models.DateTimeField(db_column='FH_Cita')),
                ('fh_conclusion', models.DateTimeField(db_column='FH_Conclusion')),
                ('secretaria_field', models.CharField(db_column='Secretaria=>', max_length=12)),
                ('nombre_secretaria', models.CharField(db_column='Nombre_Secretaria', max_length=50)),
                ('apellido_secretaria', models.CharField(blank=True, db_column='Apellido_Secretaria', max_length=50, null=True)),
                ('dni_secretaria', models.CharField(db_column='DNI_Secretaria', max_length=20)),
                ('sexo_secretaria', models.CharField(blank=True, db_column='Sexo_Secretaria', max_length=13, null=True)),
                ('agente_inmobiliatio_field', models.CharField(db_column='Agente Inmobiliatio=>', max_length=21)),
                ('nombre_ai', models.CharField(db_column='Nombre_AI', max_length=50)),
                ('apellido_ai', models.CharField(blank=True, db_column='Apellido_AI', max_length=50, null=True)),
                ('dni_ai', models.CharField(db_column='DNI_AI', max_length=20)),
                ('sexo_ai', models.CharField(blank=True, db_column='Sexo_AI', max_length=13, null=True)),
                ('cliente_field', models.CharField(db_column='Cliente=>', max_length=9)),
                ('nombre_cliente', models.CharField(db_column='Nombre_Cliente', max_length=50)),
                ('apellido_cliente', models.CharField(blank=True, db_column='Apellido_Cliente', max_length=50, null=True)),
                ('dni_cliente', models.CharField(db_column='DNI_Cliente', max_length=20)),
                ('sexo_cliente', models.CharField(blank=True, db_column='Sexo_Cliente', max_length=13, null=True)),
                ('propiedad_field', models.CharField(db_column='Propiedad=>', max_length=11)),
                ('ciudad_prop', models.CharField(db_column='Ciudad_Prop', max_length=20)),
                ('provincia_prop', models.CharField(db_column='Provincia_Prop', max_length=20)),
                ('pais_prop', models.CharField(db_column='Pais_Prop', max_length=20)),
                ('direccion_prop', models.CharField(db_column='Direccion_Prop', max_length=100)),
                ('tipo_prop', models.CharField(db_column='Tipo_Prop', max_length=12)),
                ('pisos_prop', models.PositiveIntegerField(db_column='Pisos_Prop')),
                ('metros_cuadrados_prop', models.DecimalField(db_column='Metros_Cuadrados_Prop', decimal_places=0, max_digits=10)),
                ('estado_prop', models.CharField(db_column='Estado_Prop', max_length=8)),
                ('dueño_field', models.CharField(db_column='Dueño=>', max_length=7)),
                ('nombre_dueño', models.CharField(db_column='Nombre_Dueño', max_length=50)),
                ('apellido_dueño', models.CharField(blank=True, db_column='Apellido_Dueño', max_length=50, null=True)),
                ('dni_dueño', models.CharField(db_column='DNI_Dueño', max_length=20)),
                ('sexo_dueño', models.CharField(blank=True, db_column='Sexo_Dueño', max_length=13, null=True)),
            ],
            options={
                'db_table': 'registro_de_citas',
            },
        ),
        migrations.CreateModel(
            name='Transaccion',
            fields=[
                ('nro_transaccion', models.AutoField(db_column='NRO_Transaccion', primary_key=True, serialize=False)),
                ('f_creacion_transaccion', models.DateField(db_column='F_Creacion_Transaccion')),
                ('h_creacion_transaccion', models.TimeField(db_column='H_Creacion_Transaccion')),
                ('monto_transaccion', models.DecimalField(db_column='Monto_Transaccion', decimal_places=0, max_digits=10)),
                ('tipo_transaccion', models.CharField(choices=[('PS', 'Pago Sueldo'), ('CA', 'Cobro Alquiler'), ('PA', 'Pago Alquiler'), ('CV', 'Cobro Venta'), ('PV', 'Pago Venta')], db_column='Tipo_Transaccion', max_length=14)),
                ('descripcion_transaccion', models.CharField(blank=True, db_column='Descripcion_Transaccion', max_length=100, null=True)),
                ('cajera_responsable_transaccion', models.ForeignKey(db_column='Cajera_Responsable_Transaccion', on_delete=django.db.models.deletion.RESTRICT, related_name='cajera_transac', to=settings.AUTH_USER_MODEL)),
                ('client_paga_cobra_transaccion', models.ForeignKey(blank=True, db_column='Client_Paga-Cobra_Transaccion', null=True, on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
                ('emp_cobra_transaccion', models.ForeignKey(blank=True, db_column='Emp_Cobra_Transaccion', null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='emp_transac', to=settings.AUTH_USER_MODEL)),
                ('id_caja_transaccion', models.ForeignKey(db_column='ID_Caja_Transaccion', on_delete=django.db.models.deletion.RESTRICT, to='user.caja')),
                ('prop_involucrada_transaccion', models.ForeignKey(blank=True, db_column='Prop_Involucrada_Transaccion', null=True, on_delete=django.db.models.deletion.RESTRICT, to='user.propiedad')),
            ],
            options={
                'db_table': 'transaccion',
            },
        ),
        migrations.CreateModel(
            name='TransaccionRutaDocumento',
            fields=[
                ('id_transaccion_ruta_documento', models.AutoField(db_column='ID_Transaccion_Ruta_Documento', primary_key=True, serialize=False)),
                ('ruta_dt', models.CharField(db_column='Ruta_DT', max_length=100)),
                ('nro_transaccion_documento', models.ForeignKey(db_column='NRO_Transaccion_Documento', on_delete=django.db.models.deletion.CASCADE, to='user.transaccion')),
            ],
            options={
                'db_table': 'transaccion_ruta_documento',
            },
        ),
        migrations.CreateModel(
            name='Provincia',
            fields=[
                ('id_provincia', models.AutoField(db_column='ID_Provincia', primary_key=True, serialize=False)),
                ('nombre_provincia', models.CharField(db_column='Nombre_Provincia', max_length=20)),
                ('nombre_pais_provincia', models.ForeignKey(db_column='Nombre_Pais_Provincia', on_delete=django.db.models.deletion.CASCADE, to='user.pais')),
            ],
            options={
                'verbose_name_plural': 'Provincias',
                'db_table': 'provincia',
            },
        ),
        migrations.CreateModel(
            name='PropiedadRutaImagen',
            fields=[
                ('id_propiedad_ruta_imagen', models.AutoField(db_column='ID_Propiedad_Ruta_Imagen', primary_key=True, serialize=False)),
                ('ruta_pi', models.CharField(db_column='Ruta_PI', max_length=100)),
                ('id_propiedad_imagen', models.ForeignKey(db_column='ID_Propiedad_Imagen', on_delete=django.db.models.deletion.CASCADE, to='user.propiedad')),
            ],
            options={
                'db_table': 'propiedad_ruta_imagen',
            },
        ),
        migrations.CreateModel(
            name='PropiedadRutaDocumento',
            fields=[
                ('id_propiedad_ruta_documento', models.AutoField(db_column='ID_Propiedad_Ruta_Documento', primary_key=True, serialize=False)),
                ('ruta_pd', models.ImageField(db_column='Ruta_PD', upload_to='propiedad/')),
                ('id_propiedad_documento', models.ForeignKey(db_column='ID_Propiedad_Documento', on_delete=django.db.models.deletion.CASCADE, to='user.propiedad')),
            ],
            options={
                'db_table': 'propiedad_ruta_documento',
            },
        ),
        migrations.CreateModel(
            name='PaisHablaIdioma',
            fields=[
                ('id_paishablaidioma', models.AutoField(db_column='ID_Pais_Habla_Idioma', primary_key=True, serialize=False)),
                ('nombre_idioma_idioma', models.ForeignKey(db_column='Nombre_Idioma_Idioma', on_delete=django.db.models.deletion.RESTRICT, to='user.idioma')),
                ('nombre_pais_pais', models.ForeignKey(db_column='Nombre_Pais_Pais', on_delete=django.db.models.deletion.RESTRICT, to='user.pais')),
            ],
            options={
                'db_table': 'pais_habla_idioma',
            },
        ),
        migrations.CreateModel(
            name='EmpleadoCobroPendiente',
            fields=[
                ('nro_cobro', models.AutoField(db_column='NRO_Cobro', primary_key=True, serialize=False)),
                ('f_creacion_cobrop', models.DateField(db_column='F_Creacion_CobroP')),
                ('h_creacion_cobrop', models.TimeField(db_column='H_Creacion_CobroP')),
                ('monto_cobro_empleado', models.DecimalField(db_column='Monto_Cobro_Empleado', decimal_places=0, max_digits=10)),
                ('descripcion_cobro_empleado', models.CharField(blank=True, db_column='Descripcion_Cobro_Empleado', max_length=100, null=True)),
                ('tipo_cobro_empleado', models.CharField(choices=[('SU', 'Sueldo'), ('COM', 'Comision')], db_column='Tipo_Cobro_Empleado', max_length=8)),
                ('id_empleado_cobra', models.ForeignKey(db_column='ID_Empleado_Cobra', on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'empleado_cobro_pendiente',
            },
        ),
        migrations.CreateModel(
            name='DeudaCliente',
            fields=[
                ('nro_deuda_cliente', models.AutoField(db_column='NRO_Deuda_Cliente', primary_key=True, serialize=False)),
                ('f_creacion_deuda', models.DateField(db_column='F_Creacion_Deuda')),
                ('monto_deuda', models.DecimalField(db_column='Monto_Deuda', decimal_places=0, max_digits=10)),
                ('id_cliente_debe', models.ForeignKey(db_column='ID_Cliente_Debe', on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
                ('id_propiedad_deuda', models.ForeignKey(db_column='ID_Propiedad_Deuda', on_delete=django.db.models.deletion.RESTRICT, to='user.propiedad')),
            ],
            options={
                'db_table': 'deuda_cliente',
            },
        ),
        migrations.CreateModel(
            name='ContratoRutaDocumento',
            fields=[
                ('id_contrato_ruta_documento', models.AutoField(db_column='ID_Contrato_Ruta_Documento', primary_key=True, serialize=False)),
                ('ruta_cd', models.CharField(db_column='Ruta_CD', max_length=100)),
                ('nro_contrato_documento', models.ForeignKey(db_column='NRO_Contrato_Documento', on_delete=django.db.models.deletion.CASCADE, to='user.contratocerrado')),
            ],
            options={
                'db_table': 'contrato_ruta_documento',
            },
        ),
        migrations.AddField(
            model_name='contratocerrado',
            name='prop_involucrada_contrato',
            field=models.ForeignKey(db_column='Prop_Involucrada_Contrato', on_delete=django.db.models.deletion.CASCADE, to='user.propiedad'),
        ),
        migrations.CreateModel(
            name='CobroPendCliente',
            fields=[
                ('nro_cobro_p_cliente', models.AutoField(db_column='NRO_Cobro_P_Cliente', primary_key=True, serialize=False)),
                ('f_creacion_cobro_pc', models.DateField(db_column='F_Creacion_Cobro_PC')),
                ('monto_cobro_pc', models.DecimalField(db_column='Monto_Cobro_PC', decimal_places=0, max_digits=10)),
                ('id_cliente_cobra', models.ForeignKey(db_column='ID_Cliente_Cobra', on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
                ('id_prop_involuc_cpc', models.ForeignKey(db_column='ID_Prop_Involuc_CPC', on_delete=django.db.models.deletion.RESTRICT, to='user.propiedad')),
            ],
            options={
                'db_table': 'cobro_pend_cliente',
            },
        ),
        migrations.AddField(
            model_name='ciudad',
            name='id_provincia_ciudad',
            field=models.ForeignKey(db_column='ID_Provincia_Ciudad', on_delete=django.db.models.deletion.CASCADE, to='user.provincia'),
        ),
        migrations.CreateModel(
            name='Cita',
            fields=[
                ('nro_cita', models.AutoField(db_column='NRO_Cita', primary_key=True, serialize=False, verbose_name='Cita N°')),
                ('f_creacion_cita', models.DateField(auto_now_add=True, db_column='F_Creacion_Cita')),
                ('h_creacion_cita', models.TimeField(auto_now_add=True, db_column='H_Creacion_Cita')),
                ('f_asignacion_cita', models.DateField(blank=True, db_column='F_Asignacion_Cita', null=True)),
                ('h_asignacion_cita', models.TimeField(blank=True, db_column='H_Asignacion_Cita', null=True)),
                ('f_cita', models.DateField(db_column='F_Cita', null=True, verbose_name='Fecha')),
                ('h_cita', models.TimeField(db_column='H_Cita', null=True, verbose_name='Hora')),
                ('f_concluye_cita', models.DateField(blank=True, db_column='F_Concluye_Cita', null=True)),
                ('h_concluye_cita', models.TimeField(blank=True, db_column='H_Concluye_Cita', null=True)),
                ('tipo_cita', models.CharField(choices=[('SOL', 'Solicitud'), ('AG', 'Agendada')], db_column='Tipo_Cita', max_length=9, verbose_name='Cita de tipo')),
                ('ai_atiende_cita', models.ForeignKey(blank=True, db_column='AI_Atiende_Cita', limit_choices_to={'tipo_usuario': 'EAI'}, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='ai_cita', to=settings.AUTH_USER_MODEL, verbose_name='Agente inmobiliario asignado')),
                ('client_solicita_cita', models.ForeignKey(db_column='Client_Solicita_Cita', limit_choices_to=models.Q(('tipo_usuario', 'CP'), ('tipo_usuario', 'CC'), _connector='OR'), on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL, verbose_name='Cliente quien solicita')),
                ('propiedad_involucrada', models.ForeignKey(db_column='Propiedad_Involucrada', on_delete=django.db.models.deletion.CASCADE, to='user.propiedad', verbose_name='Codigo de propiedad')),
                ('secre_asigna_cita', models.ForeignKey(blank=True, db_column='Secre_Asigna_Cita', limit_choices_to={'tipo_usuario': 'ES'}, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='secre_cita', to=settings.AUTH_USER_MODEL, verbose_name='Secretaria a cargo')),
            ],
            options={
                'verbose_name_plural': 'Listado de Citas',
                'db_table': 'cita',
            },
        ),
        migrations.CreateModel(
            name='CierreCaja',
            fields=[
                ('id_cierre_caja', models.AutoField(db_column='ID_Cierre_Caja', primary_key=True, serialize=False)),
                ('fecha_cierre_caja', models.DateField(db_column='Fecha_Cierre_Caja')),
                ('monto_cierre', models.DecimalField(db_column='Monto_Cierre', decimal_places=0, max_digits=10)),
                ('id_caja_cierre', models.ForeignKey(db_column='ID_Caja_Cierre', on_delete=django.db.models.deletion.RESTRICT, to='user.caja')),
            ],
            options={
                'db_table': 'cierre_caja',
            },
        ),
        migrations.CreateModel(
            name='AiAtiendeCiudad',
            fields=[
                ('id_ai_atiende_ciudad', models.AutoField(db_column='ID_AI_Atiende_Ciudad', primary_key=True, serialize=False)),
                ('id_ai', models.ForeignKey(db_column='ID_AI', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('id_ciudad_ai_atiende_ciudad', models.ForeignKey(db_column='ID_Ciudad_AIatiendeCiudad', on_delete=django.db.models.deletion.RESTRICT, to='user.ciudad')),
            ],
            options={
                'db_table': 'ai_atiende_ciudad',
            },
        ),
        migrations.AddConstraint(
            model_name='transaccionrutadocumento',
            constraint=models.UniqueConstraint(fields=('nro_transaccion_documento', 'ruta_dt'), name='TransaccionRutaDocumento_pk'),
        ),
        migrations.AddConstraint(
            model_name='provincia',
            constraint=models.UniqueConstraint(fields=('nombre_provincia', 'nombre_pais_provincia'), name='Provincia_pk'),
        ),
        migrations.AddConstraint(
            model_name='propiedadrutaimagen',
            constraint=models.UniqueConstraint(fields=('id_propiedad_imagen', 'ruta_pi'), name='PropiedadRutaImagen_pk'),
        ),
        migrations.AddConstraint(
            model_name='propiedadrutadocumento',
            constraint=models.UniqueConstraint(fields=('id_propiedad_documento', 'ruta_pd'), name='PropiedadRutaDocumento_pk'),
        ),
        migrations.AddConstraint(
            model_name='propiedad',
            constraint=models.UniqueConstraint(fields=('direccion', 'id_ciudad_propiedad'), name='Unica_Direccion'),
        ),
        migrations.AddConstraint(
            model_name='paishablaidioma',
            constraint=models.UniqueConstraint(fields=('nombre_idioma_idioma', 'nombre_pais_pais'), name='PaisHablaIdioma_pk'),
        ),
        migrations.AddConstraint(
            model_name='contratorutadocumento',
            constraint=models.UniqueConstraint(fields=('nro_contrato_documento', 'ruta_cd'), name='Contrato_Ruta_Documento_pk'),
        ),
        migrations.AddConstraint(
            model_name='ciudad',
            constraint=models.UniqueConstraint(fields=('nombre_ciudad', 'id_provincia_ciudad'), name='Ciudad_pk'),
        ),
        migrations.AddConstraint(
            model_name='cierrecaja',
            constraint=models.UniqueConstraint(fields=('id_caja_cierre', 'fecha_cierre_caja'), name='CierreCaja_pk'),
        ),
        migrations.AddConstraint(
            model_name='aiatiendeciudad',
            constraint=models.UniqueConstraint(fields=('id_ciudad_ai_atiende_ciudad', 'id_ai'), name='AIAtiendeCiudad_pk'),
        ),
    ]
