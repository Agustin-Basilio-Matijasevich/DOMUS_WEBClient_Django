from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import ManagerUsuario

# Create your models here
class Usuario(AbstractBaseUser, PermissionsMixin):
    SEXO = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('NE', 'No Especifica'),
    )
    TIPO_USUARIO = (
        ('ES', 'Empleado_Secretario'),
        ('EAI','Empleado_Agente Inmobiliario'),
        ('EM','Empleado_Marketing'),
        ('EJD','Empleado_Jefe de Departamento'),
        ('EC','Empleado_Cajero'),
        ('EAS','Empleado_Administrador de Sistema'),
        ('EGG','Empleado_Gerente General'),
        ('CP','Cliente_Particular'),
        ('CC','Cliente_Corporativo'),
    )
    username = models.CharField(max_length=20, unique=True)
    dni = models.PositiveIntegerField()  # Field name made lowercase.
    email = models.CharField(max_length=50, null=True, blank=True)
    nombres = models.CharField(max_length=50)  # Field name made lowercase.
    apellidos = models.CharField(max_length=50, null=True, blank=True)  # Field name made lowercase.
    sexo = models.CharField(choices=SEXO, max_length=10, null=True, default='NE')  # Field name made lowercase.
    salario_mensual = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)  # Field name made lowercase.
    departamento = models.CharField(max_length=16, null=True, blank=True)  # Field name made lowercase.
    foto_perfil = models.TextField(blank=True, null=True)  # Field name made lowercase.
    tipo_usuario = models.CharField(choices=TIPO_USUARIO, max_length=50)  # Field name made lowercase.    
    is_staff= models.BooleanField(default=False)
    objects = ManagerUsuario()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['dni','nombres','tipo_usuario',]
    
    class Meta:
        db_table = 'usuario'
    
    
class Idioma(models.Model):
    nombre_idioma = models.CharField(db_column='Nombre_Idioma', primary_key=True, max_length=20)  # Field name made lowercase.

    class Meta:
        db_table = 'idioma'
        
        
class Pais(models.Model):
    nombre_pais = models.CharField(db_column='Nombre_Pais', primary_key=True, max_length=20)  # Field name made lowercase.

    class Meta:
        db_table = 'pais'
        
        
class PaisHablaIdioma(models.Model):
    nombre_idioma_idioma = models.OneToOneField(Idioma, models.DO_NOTHING, db_column='Nombre_Idioma_Idioma', primary_key=True)  # Field name made lowercase.
    nombre_pais_pais = models.ForeignKey(Pais, models.DO_NOTHING, db_column='Nombre_Pais_Pais')  # Field name made lowercase.

    class Meta:
        db_table = 'pais_habla_idioma'
        unique_together = (('nombre_idioma_idioma', 'nombre_pais_pais'),)
        
        
class Provincia(models.Model):
    nombre_provincia = models.CharField(db_column='Nombre_Provincia', primary_key=True, max_length=20)  # Field name made lowercase.
    nombre_pais_provincia = models.ForeignKey(Pais, models.DO_NOTHING, db_column='Nombre_Pais_Provincia')  # Field name made lowercase.

    class Meta:
        db_table = 'provincia'
        unique_together = (('nombre_provincia', 'nombre_pais_provincia'),)
        
        
class Ciudad(models.Model):
    nombre_ciudad = models.CharField(db_column='Nombre_Ciudad', primary_key=True, max_length=20)  # Field name made lowercase.
    nombre_provincia_ciudad = models.ForeignKey(Provincia, models.DO_NOTHING, db_column='Nombre_Provincia_Ciudad', related_name='Nombre_Provincia')  # Field name made lowercase.
    nombre_pais_ciudad = models.ForeignKey(Provincia, models.DO_NOTHING, db_column='Nombre_Pais_Ciudad', related_name='Nombre_Pais_Provincia')  # Field name made lowercase.

    class Meta:
        db_table = 'ciudad'
        unique_together = (('nombre_ciudad', 'nombre_provincia_ciudad', 'nombre_pais_ciudad'),)
        
        
class AiAtiendeCiudad(models.Model):
    nombre_ciudad_ai = models.OneToOneField(Ciudad, models.DO_NOTHING, db_column='Nombre_Ciudad_AI', primary_key=True, related_name='Nombre_Ciudad_AI')  # Field name made lowercase.
    nombre_provincia_ai = models.ForeignKey(Ciudad, models.DO_NOTHING, db_column='Nombre_Provincia_AI', related_name='Nombre_Provincia_AI')  # Field name made lowercase.
    nombre_pais_ai = models.ForeignKey(Ciudad, models.DO_NOTHING, db_column='Nombre_Pais_AI', related_name='Nombre_Pais_AI')  # Field name made lowercase.
    id_ai = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='ID_AI')  # Field name made lowercase.

    class Meta:
        db_table = 'ai_atiende_ciudad'
        unique_together = (('nombre_ciudad_ai', 'nombre_provincia_ai', 'nombre_pais_ai', 'id_ai'),)
        
        
class Propiedad(models.Model):
    TIPO_PROPIEDAD = (
        	('CAS', 'Casa'),
        	('DEP', 'Departamento'),
        	('GAL', 'Galpon'),
        	('CAMP', 'Campo'),
        	('TER', 'Terreno'),
    	)
    ESTADO_PROPIEDAD = (
        ('VEN', 'Venta'),
        ('ALQ','Alquiler'),
    )
    id_propiedad = models.AutoField(db_column='ID_Propiedad', primary_key=True)  # Field name made lowercase.
    id_dueño = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='ID_Dueño')  # Field name made lowercase.
    id_adquiere_o_alquila = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='ID_Adquiere_o_Alquila', blank=True, null=True)  # Field name made lowercase.
    nombre_ciudad_propiedad = models.ForeignKey(Ciudad, models.DO_NOTHING, db_column='Nombre_Ciudad_Propiedad')  # Field name made lowercase.
    nombre_provincia_propiedad = models.ForeignKey(Ciudad, models.DO_NOTHING, db_column='Nombre_Provincia_Propiedad', to_field='Nombre_Provincia_Ciudad')  # Field name made lowercase.
    nombre_pais_propiedad = models.ForeignKey(Ciudad, models.DO_NOTHING, db_column='Nombre_Pais_Propiedad', to_field='Nombre_Pais_Ciudad')  # Field name made lowercase.
    tipo_propiedad = models.CharField(choices=TIPO_PROPIEDAD, db_column='Tipo_Propiedad', max_length=12)  # Field name made lowercase.
    pisos = models.PositiveIntegerField(db_column='Pisos')  # Field name made lowercase.
    metros_cuadrados = models.DecimalField(db_column='Metros_Cuadrados', max_digits=10, decimal_places=0)  # Field name made lowercase.
    direccion = models.CharField(db_column='Direccion', max_length=100)  # Field name made lowercase.
    estado_propiedad = models.CharField(choices=ESTADO_PROPIEDAD, db_column='Estado_Propiedad', max_length=8)  # Field name made lowercase.

    class Meta:
        db_table = 'propiedad'


class PropiedadRutaDocumento(models.Model):
    id_propiedad_documento = models.OneToOneField(Propiedad, models.DO_NOTHING, db_column='ID_Propiedad_Documento', primary_key=True)  # Field name made lowercase.
    ruta_pd = models.CharField(db_column='Ruta_PD', max_length=100)  # Field name made lowercase.

    class Meta:
        db_table = 'propiedad_ruta_documento'
        unique_together = (('id_propiedad_documento', 'ruta_pd'),)


class PropiedadRutaImagen(models.Model):
    id_propiedad_imagen = models.OneToOneField(Propiedad, models.DO_NOTHING, db_column='ID_Propiedad_Imagen', primary_key=True)  # Field name made lowercase.
    ruta_pi = models.CharField(db_column='Ruta_PI', max_length=100)  # Field name made lowercase.

    class Meta:
        db_table = 'propiedad_ruta_imagen'
        unique_together = (('id_propiedad_imagen', 'ruta_pi'),)


class Cita(models.Model):
    TIPO_CITA = (
        	('SOL', 'Solicitud'),
        	('AG', 'Agendada'),
    )
    nro_cita = models.AutoField(db_column='NRO_Cita', primary_key=True)  # Field name made lowercase.
    f_creacion_cita = models.DateField(db_column='F_Creacion_Cita')  # Field name made lowercase.
    h_creacion_cita = models.TimeField(db_column='H_Creacion_Cita')  # Field name made lowercase.
    f_asignacion_cita = models.DateField(db_column='F_Asignacion_Cita', blank=True, null=True)  # Field name made lowercase.
    h_asignacion_cita = models.TimeField(db_column='H_Asignacion_Cita', blank=True, null=True)  # Field name made lowercase.
    f_cita = models.DateField(db_column='F_Cita', blank=True, null=True)  # Field name made lowercase.
    h_cita = models.TimeField(db_column='H_Cita', blank=True, null=True)  # Field name made lowercase.
    f_concluye_cita = models.DateField(db_column='F_Concluye_Cita', blank=True, null=True)  # Field name made lowercase.
    h_concluye_cita = models.TimeField(db_column='H_Concluye_Cita', blank=True, null=True)  # Field name made lowercase.
    secre_asigna_cita = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='Secre_Asigna_Cita', blank=True, null=True, related_name='Secre_Asigna_Cita')  # Field name made lowercase.
    ai_atiende_cita = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='AI_Atiende_Cita', blank=True, null=True, related_name='AI_Atiende_Cita')  # Field name made lowercase.
    client_solicita_cita = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='Client_Solicita_Cita', related_name='Client_Solicita_Cita')  # Field name made lowercase.
    propiedad_involucrada = models.ForeignKey(Propiedad, models.DO_NOTHING, db_column='Propiedad_Involucrada', related_name='Client_Solicita_Cita')  # Field name made lowercase.
    tipo_cita = models.CharField(choices=TIPO_CITA, db_column='Tipo_Cita', max_length=9)  # Field name made lowercase.

    class Meta:
        db_table = 'cita'


class ContratoCerrado(models.Model):
    TIPO_CONTRATO = (
        	('VEN', 'Venta'),
        	('ALQ','Alquiler'),
    )
    nro_contrato = models.AutoField(db_column='NRO_Contrato', primary_key=True)  # Field name made lowercase.
    f_creacion_contrato = models.DateField(db_column='F_Creacion_Contrato')  # Field name made lowercase.
    f_caduca_contrato = models.DateField(db_column='F_Caduca_Contrato', blank=True, null=True)  # Field name made lowercase.
    monto = models.DecimalField(db_column='Monto', max_digits=10, decimal_places=0)  # Field name made lowercase.
    tipo_contrato = models.CharField(choices=TIPO_CONTRATO, db_column='Tipo_Contrato', max_length=8)  # Field name made lowercase.
    ai_responsable_contrato = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='AI_Responsable_Contrato', related_name='AI_Responsable_Contrato')  # Field name made lowercase.
    client_involucrado_contrato = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='Client_Involucrado_Contrato', related_name='Client_Involucrado_Contrato')  # Field name made lowercase.
    prop_involucrada_contrato = models.ForeignKey(Propiedad, models.DO_NOTHING, db_column='Prop_Involucrada_Contrato', related_name='Prop_Involucrada_Contrato')  # Field name made lowercase.

    class Meta:
        db_table = 'contrato_cerrado'


class ContratoRutaDocumento(models.Model):
    nro_contrato_documento = models.OneToOneField(ContratoCerrado, models.DO_NOTHING, db_column='NRO_Contrato_Documento', primary_key=True)  # Field name made lowercase.
    ruta_cd = models.CharField(db_column='Ruta_CD', max_length=100)  # Field name made lowercase.

    class Meta:
        db_table = 'contrato_ruta_documento'
        unique_together = (('nro_contrato_documento', 'ruta_cd'),)


class EmpleadoCobroPendiente(models.Model):
    TIPO_COBRO_EMPLEADO = (
        	('SU', 'Sueldo'),
        	('COM','Comision'),
    )
    nro_cobro = models.AutoField(db_column='NRO_Cobro', primary_key=True)  # Field name made lowercase.
    id_empleado_cobra = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='ID_Empleado_Cobra')  # Field name made lowercase.
    f_creacion_cobrop = models.DateField(db_column='F_Creacion_CobroP')  # Field name made lowercase.
    h_creacion_cobrop = models.TimeField(db_column='H_Creacion_CobroP')  # Field name made lowercase.
    monto_cobro_empleado = models.DecimalField(db_column='Monto_Cobro_Empleado', max_digits=10, decimal_places=0)  # Field name made lowercase.
    descripcion_cobro_empleado = models.CharField(db_column='Descripcion_Cobro_Empleado', max_length=100, blank=True, null=True)  # Field name made lowercase.
    tipo_cobro_empleado = models.CharField(choices=TIPO_COBRO_EMPLEADO, db_column='Tipo_Cobro_Empleado', max_length=8)  # Field name made lowercase.

    class Meta:
        db_table = 'empleado_cobro_pendiente'


class Caja(models.Model):
    BIT = (
        	('SI', 'Abierta'),
        	('NO','Cerrada'),
    )
    id_caja = models.AutoField(db_column='ID_Caja', primary_key=True)  # Field name made lowercase.
    descripcion_caja = models.CharField(db_column='Descripcion_Caja', max_length=100)  # Field name made lowercase.
    isopen = models.CharField(choices=BIT, db_column='IsOpen', default='NO', max_length=8)  # Field name made lowercase. This field type is a guess.

    class Meta:
        db_table = 'caja'


class CierreCaja(models.Model):
    id_caja_cierre = models.OneToOneField(Caja, models.DO_NOTHING, db_column='ID_Caja_Cierre', primary_key=True)  # Field name made lowercase.
    fecha_cierre_caja = models.DateField(db_column='Fecha_Cierre_Caja')  # Field name made lowercase.
    monto_cierre = models.DecimalField(db_column='Monto_Cierre', max_digits=10, decimal_places=0)  # Field name made lowercase.

    class Meta:
        db_table = 'cierre_caja'
        unique_together = (('id_caja_cierre', 'fecha_cierre_caja'),)


class Transaccion(models.Model):
    TIPO_TRANSACCION = (
        	('PS', 'Pago Sueldo'),
        	('CA', 'Cobro Alquiler'),
        	('PA', 'Pago Alquiler'),
        	('CV', 'Cobro Venta'),
        	('PV', 'Pago Venta'),
    )
    nro_transaccion = models.AutoField(db_column='NRO_Transaccion', primary_key=True)  # Field name made lowercase.
    f_creacion_transaccion = models.DateField(db_column='F_Creacion_Transaccion')  # Field name made lowercase.
    h_creacion_transaccion = models.TimeField(db_column='H_Creacion_Transaccion')  # Field name made lowercase.
    monto_transaccion = models.DecimalField(db_column='Monto_Transaccion', max_digits=10, decimal_places=0)  # Field name made lowercase.
    tipo_transaccion = models.CharField(choices=TIPO_TRANSACCION, db_column='Tipo_Transaccion', max_length=14)  # Field name made lowercase.
    descripcion_transaccion = models.CharField(db_column='Descripcion_Transaccion', max_length=100, blank=True, null=True)  # Field name made lowercase.
    id_caja_transaccion = models.ForeignKey(Caja, models.DO_NOTHING, db_column='ID_Caja_Transaccion', related_name='ID_Caja_Transaccion')  # Field name made lowercase.
    cajera_responsable_transaccion = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='Cajera_Responsable_Transaccion', related_name='Cajera_Responsable_Transaccion')  # Field name made lowercase.
    emp_cobra_transaccion = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='Emp_Cobra_Transaccion', blank=True, null=True, related_name='Emp_Cobra_Transaccion')  # Field name made lowercase.
    client_paga_cobra_transaccion = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='Client_Paga-Cobra_Transaccion', blank=True, null=True, related_name='Client_Paga-Cobra_Transaccion')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    prop_involucrada_transaccion = models.ForeignKey(Propiedad, models.DO_NOTHING, db_column='Prop_Involucrada_Transaccion', blank=True, null=True, related_name='Prop_Involucrada_Transaccion')  # Field name made lowercase.

    class Meta:
        db_table = 'transaccion'


class TransaccionRutaDocumento(models.Model):
    nro_transaccion_documento = models.OneToOneField(Transaccion, models.DO_NOTHING, db_column='NRO_Transaccion_Documento', primary_key=True)  # Field name made lowercase.
    ruta_dt = models.CharField(db_column='Ruta_DT', max_length=100)  # Field name made lowercase.

    class Meta:
        db_table = 'transaccion_ruta_documento'
        unique_together = (('nro_transaccion_documento', 'ruta_dt'),)


class DeudaCliente(models.Model):
    nro_deuda_cliente = models.AutoField(db_column='NRO_Deuda_Cliente', primary_key=True)  # Field name made lowercase.
    f_creacion_deuda = models.DateField(db_column='F_Creacion_Deuda')  # Field name made lowercase.
    monto_deuda = models.DecimalField(db_column='Monto_Deuda', max_digits=10, decimal_places=0)  # Field name made lowercase.
    id_cliente_debe = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='ID_Cliente_Debe')  # Field name made lowercase.
    id_propiedad_deuda = models.ForeignKey(Propiedad, models.DO_NOTHING, db_column='ID_Propiedad_Deuda')  # Field name made lowercase.

    class Meta:
        db_table = 'deuda_cliente'
        
        
class CobroPendCliente(models.Model):
    nro_cobro_p_cliente = models.AutoField(db_column='NRO_Cobro_P_Cliente', primary_key=True)  # Field name made lowercase.
    f_creacion_cobro_pc = models.DateField(db_column='F_Creacion_Cobro_PC')  # Field name made lowercase.
    monto_cobro_pc = models.DecimalField(db_column='Monto_Cobro_PC', max_digits=10, decimal_places=0)  # Field name made lowercase.
    id_cliente_cobra = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='ID_Cliente_Cobra')  # Field name made lowercase.
    id_prop_involuc_cpc = models.ForeignKey(Propiedad, models.DO_NOTHING, db_column='ID_Prop_Involuc_CPC')  # Field name made lowercase.

    class Meta:
        db_table = 'cobro_pend_cliente'