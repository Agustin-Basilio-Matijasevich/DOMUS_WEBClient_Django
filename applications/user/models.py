from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import ManagerUsuario
from django.db.models import Q
import os
from datetime import date
import datetime
from django.utils import timezone
from uuid import uuid4

class Usuario(AbstractBaseUser, PermissionsMixin):
    def generateRutaUsuarios(instance, filename):
        #Extraemos la extension de la imagen guardada: *.jpg|*.png, etc.
        extensionImagen = os.path.splitext(filename)[1][1:]
        #Generacion de ruta relativa a MEDIA_ROOT: Propiedades/yyyy-mm/
        rutaImagen = os.path.join('Usuarios', date.today().strftime("%Y-%m"))
        #Generamos un nombre para el archivo(random), junto con la extension: "342ewrw2342.jpg"(ejemplo)
        nombre_archivo = '{}.{}'.format(uuid4().hex, extensionImagen)
        
        #Unimos con os.path, la MEDIA_ROOT, junto con el archivo: Propiedades/yyyy-mm/342ewrw2342.jpg (ejemplo)
        return os.path.join(rutaImagen, nombre_archivo)
    
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
    DEPARTAMENTO = (
        ('COM', 'Comercializacion'),
        ('ADM', 'Administracion'),
    )
    username = models.CharField(max_length=20, unique=True)
    dni_cuil = models.CharField(max_length=20)  # Field name made lowercase.
    email = models.CharField(max_length=50, null=True)
    nombres = models.CharField(max_length=50)  # Field name made lowercase.
    apellidos = models.CharField(max_length=50, null=True)  # Field name made lowercase.
    sexo = models.CharField(choices=SEXO, max_length=10, default='NE')  # Field name made lowercase.
    salario_mensual = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)  # Field name made lowercase.
    departamento = models.CharField(choices=DEPARTAMENTO, max_length=16, null=True, blank=True)  # Field name made lowercase.
    foto_perfil = models.ImageField(upload_to=generateRutaUsuarios, max_length=100)  # Field name made lowercase.
    tipo_usuario = models.CharField(choices=TIPO_USUARIO, max_length=10)  # Field name made lowercase.
    is_staff= models.BooleanField(default=False)
    objects = ManagerUsuario()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['dni_cuil','nombres','apellidos','tipo_usuario',]

    class Meta:
        db_table = 'usuario'
        verbose_name = "Usuario"
        verbose_name_plural="Listado de Usuarios"

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

class Idioma(models.Model):
    nombre_idioma = models.CharField(db_column='Nombre_Idioma', primary_key=True, max_length=20)  # Field name made lowercase.

    class Meta:
        db_table = 'idioma'


class Pais(models.Model):
    nombre_pais = models.CharField(db_column='Nombre_Pais', primary_key=True, max_length=20)  # Field name made lowercase.

    class Meta:
        db_table = 'pais'
        verbose_name = "Pais"
        verbose_name_plural="Listado de Paises"

    def __str__(self):
        return self.nombre_pais
    
class PaisHablaIdioma(models.Model):
    id_paishablaidioma = models.AutoField(db_column='ID_Pais_Habla_Idioma', primary_key=True)
    nombre_idioma_idioma = models.ForeignKey(Idioma, db_column='Nombre_Idioma_Idioma', on_delete=models.RESTRICT)  # Field name made lowercase.
    nombre_pais_pais = models.ForeignKey(Pais, db_column='Nombre_Pais_Pais', on_delete=models.RESTRICT)  # Field name made lowercase.

    class Meta:
        db_table = 'pais_habla_idioma'
        constraints = [models.UniqueConstraint(fields=['nombre_idioma_idioma', 'nombre_pais_pais'], name='PaisHablaIdioma_pk')]


class Provincia(models.Model):
    id_provincia = models.AutoField(db_column='ID_Provincia', primary_key=True)
    nombre_provincia = models.CharField(db_column='Nombre_Provincia', max_length=20)  # Field name made lowercase.
    nombre_pais_provincia = models.ForeignKey(Pais, db_column='Nombre_Pais_Provincia', on_delete=models.CASCADE)  # Field name made lowercase.

    class Meta:
        db_table = 'provincia'
        verbose_name = "Provincia"
        verbose_name_plural="Listado de Provincias"
        constraints = [models.UniqueConstraint(fields=['nombre_provincia', 'nombre_pais_provincia'], name='Provincia_pk')]

    def __str__(self):
        return self.nombre_provincia

class Ciudad(models.Model):
    id_ciudad = models.AutoField(db_column='ID_Ciudad', primary_key=True)
    nombre_ciudad = models.CharField(db_column='Nombre_Ciudad', max_length=20)  # Field name made lowercase.
    id_provincia_ciudad = models.ForeignKey(Provincia, db_column='ID_Provincia_Ciudad', on_delete=models.CASCADE)  # Field name made lowercase.

    class Meta:
        db_table = 'ciudad'
        verbose_name = "Ciudad"
        verbose_name_plural="Listado de Ciudades"
        constraints = [models.UniqueConstraint(fields=['nombre_ciudad', 'id_provincia_ciudad'], name='Ciudad_pk')]

    def __str__(self):
        return self.nombre_ciudad
    
class AiAtiendeCiudad(models.Model):
    id_ai_atiende_ciudad = models.AutoField(db_column='ID_AI_Atiende_Ciudad', primary_key=True)
    id_ciudad_ai_atiende_ciudad = models.ForeignKey(Ciudad, db_column='ID_Ciudad_AIatiendeCiudad', on_delete=models.RESTRICT)  # Field name made lowercase.
    id_ai = models.ForeignKey(Usuario, db_column='ID_AI', on_delete=models.CASCADE)  # Field name made lowercase.

    class Meta:
        db_table = 'ai_atiende_ciudad'
        constraints = [models.UniqueConstraint(fields=['id_ciudad_ai_atiende_ciudad', 'id_ai'], name='AIAtiendeCiudad_pk')]


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
    id_propiedad = models.AutoField(db_column='ID_Propiedad',verbose_name="Codigo Propiedad", primary_key=True)  # Field name made lowercase.
    id_dueño = models.ForeignKey(Usuario,verbose_name="Dueño a cargo",db_column='ID_Dueño', on_delete=models.RESTRICT, related_name='dueño_propiedad', limit_choices_to=Q(tipo_usuario='CP') | Q(tipo_usuario='CC'))  # Field name made lowercase.
    id_adquiere_o_alquila = models.ForeignKey(Usuario, db_column='ID_Adquiere_o_Alquila', blank=True, null=True, on_delete=models.RESTRICT,limit_choices_to=Q(tipo_usuario='CP') | Q(tipo_usuario='CC'), verbose_name="Dueño/Inquilino")  # Field name made lowercase.
    id_ciudad_propiedad = models.ForeignKey(Ciudad,verbose_name="Ciudad donde se encuentra", db_column='ID_Ciudad_Propiedad', on_delete=models.RESTRICT)  # Field name made lowercase.
    tipo_propiedad = models.CharField(choices=TIPO_PROPIEDAD,verbose_name="Propiedad de tipo", db_column='Tipo_Propiedad', max_length=12)  # Field name made lowercase.
    pisos = models.PositiveIntegerField(db_column='Pisos',verbose_name="Piso",)  # Field name made lowercase.
    metros_cuadrados = models.DecimalField(db_column='Metros_Cuadrados',verbose_name="Metros Cuadrados", max_digits=10, decimal_places=0)  # Field name made lowercase.
    direccion = models.CharField(db_column='Direccion',verbose_name="Direccion", max_length=100)  # Field name made lowercase.
    estado_propiedad = models.CharField(choices=ESTADO_PROPIEDAD,verbose_name="Estado de la Propiedad", db_column='Estado_Propiedad', max_length=8)  # Field name made lowercase.
    precio_sugerido = models.DecimalField(db_column='Precio_Sugerido',verbose_name="Precio sugerido", max_digits=10, decimal_places=0)

    class Meta:
        db_table = 'propiedad'
        constraints = [models.UniqueConstraint(fields=['direccion', 'id_ciudad_propiedad'], name='Unica_Direccion')]
        verbose_name = "Propiedad"
        verbose_name_plural="Listado de Propiedades"

    def __str__(self):
        return f"Propiedad N°: {self.id_propiedad}"

    def CodProp(self):
        return f"COD PROP N°: {self.id_propiedad}"

    def Dueño(self):
        return f"{self.id_dueño.nombres} {self.id_dueño.apellidos}"

    def is_Disponible(self):
        if (self.id_adquiere_o_alquila is None):
            return True

        return False

    def Ubicacion(self):
        return f"{self.id_ciudad_propiedad.nombre_ciudad}, {self.id_ciudad_propiedad.id_provincia_ciudad.nombre_provincia}, {self.id_ciudad_propiedad.id_provincia_ciudad.nombre_pais_provincia.nombre_pais}"


class PropiedadRutaDocumento(models.Model):
    def generateRutaPropiedad(instance, filename):
        #Extraemos la extension de la imagen guardada: *.jpg|*.png, etc.
        extensionImagen = os.path.splitext(filename)[1][1:]
        #Generacion de ruta relativa a MEDIA_ROOT: Propiedades/yyyy-mm/
        rutaImagen = os.path.join('Propiedades', date.today().strftime("%Y-%m"))
        #Generamos un nombre para el archivo(random), junto con la extension: "342ewrw2342.jpg"(ejemplo)
        nombre_archivo = '{}.{}'.format(uuid4().hex, extensionImagen)
        
        #Unimos con os.path, la MEDIA_ROOT, junto con el archivo: Propiedades/yyyy-mm/342ewrw2342.jpg (ejemplo)
        return os.path.join(rutaImagen, nombre_archivo)
    
    id_propiedad_ruta_documento = models.AutoField(db_column='ID_Propiedad_Ruta_Documento', primary_key=True)
    id_propiedad_documento = models.ForeignKey(Propiedad, db_column='ID_Propiedad_Documento', on_delete=models.CASCADE, verbose_name="Propiedad")  # Field name made lowercase.
    ruta_pd = models.ImageField(upload_to =generateRutaPropiedad,db_column='Ruta_PD', max_length=100, verbose_name="Ruta de imagen")  # Field name made lowercase.

    #Cuando se borra el registro en la BD, tambien se borra la imagen, esto se logra sobreescribiendo el metodo delete:
    def delete(self, *args, **kwargs):
        if os.path.isfile(self.ruta_pd.path):
            os.remove(self.ruta_pd.path)

        super(PropiedadRutaDocumento, self).delete(*args, **kwargs)


    class Meta:
        verbose_name_plural = "Imagenes de Propiedades"
        verbose_name = "Imagenes de Propiedades"
        db_table = 'propiedad_ruta_documento'
        constraints = [models.UniqueConstraint(fields=['id_propiedad_documento', 'ruta_pd'], name='PropiedadRutaDocumento_pk')]

    
    def __str__(self):
        return f"Imagen - Propiedad N°{self.id_propiedad_ruta_documento}"

class PropiedadRutaImagen(models.Model):
    id_propiedad_ruta_imagen = models.AutoField(db_column='ID_Propiedad_Ruta_Imagen', primary_key=True)
    id_propiedad_imagen = models.ForeignKey(Propiedad, db_column='ID_Propiedad_Imagen', on_delete=models.CASCADE)  # Field name made lowercase.
    ruta_pi = models.CharField(db_column='Ruta_PI', max_length=100)  # Field name made lowercase.

    class Meta:
        db_table = 'propiedad_ruta_imagen'
        constraints = [models.UniqueConstraint(fields=['id_propiedad_imagen', 'ruta_pi'], name='PropiedadRutaImagen_pk')]


class Cita(models.Model):
    TIPO_CITA = (
        	('SOL', 'Solicitud'),
        	('AG', 'Agendada'),
    )
    nro_cita = models.AutoField(verbose_name="Cita N°", db_column='NRO_Cita', primary_key=True)  # Field name made lowercase.
    f_creacion_cita = models.DateField(db_column='F_Creacion_Cita', verbose_name="Fecha de creacion - Cita")  #Fecha en la que se crea la cita, independientemente del tipo de cita que sea.
    h_creacion_cita = models.TimeField(db_column='H_Creacion_Cita', verbose_name="Hora de creacion - Cita")  #Hora en la que se crea la cita, independientemente del tipo de cita que sea.
    f_asignacion_cita = models.DateField(db_column='F_Asignacion_Cita', blank=True, null=True, verbose_name="Fecha de asignacion - Cita")  # Field name made lowercase.
    h_asignacion_cita = models.TimeField(db_column='H_Asignacion_Cita', blank=True, null=True, verbose_name="Hora de asignacion - Cita")  # Field name made lowercase.
    f_cita = models.DateField(db_column='F_Cita',verbose_name='Fecha de Cita', null=True)  # Field name made lowercase.
    h_cita = models.TimeField(db_column='H_Cita',verbose_name='Hora de Cita', null=True)  # Field name made lowercase.
    f_concluye_cita = models.DateField(db_column='F_Concluye_Cita', blank=True, null=True, verbose_name="Fecha de finalizacion - Cita")  # Field name made lowercase.
    h_concluye_cita = models.TimeField(db_column='H_Concluye_Cita', blank=True, null=True, verbose_name="Hota de finalizacion - Cita")  # Field name made lowercase.
    secre_asigna_cita = models.ForeignKey(Usuario,verbose_name="Secretaria a cargo", db_column='Secre_Asigna_Cita', blank=True, null=True, on_delete=models.RESTRICT, related_name='secre_cita',limit_choices_to={'tipo_usuario':'ES'})  #Secretaria quien realiza la cita.
    ai_atiende_cita = models.ForeignKey(Usuario,verbose_name="Agente inmobiliario asignado", db_column='AI_Atiende_Cita', blank=True, null=True, on_delete=models.RESTRICT, related_name='ai_cita', limit_choices_to={'tipo_usuario':'EAI'})  #Agente, quien esta cargo esa cita.
    client_solicita_cita = models.ForeignKey(Usuario,verbose_name="Cliente quien solicita", db_column='Client_Solicita_Cita', on_delete=models.RESTRICT, limit_choices_to=Q(tipo_usuario='CP') | Q(tipo_usuario='CC')) #Cliente quien solicita la cita.
    propiedad_involucrada = models.ForeignKey(Propiedad,verbose_name="Codigo de propiedad", db_column='Propiedad_Involucrada', on_delete=models.CASCADE)  #Propiedad
    tipo_cita = models.CharField(choices=TIPO_CITA,verbose_name="Cita de tipo", db_column='Tipo_Cita', max_length=9)  #Tipo de cita, si es una solicitud o una cita agendada.

    class Meta:
        db_table = 'cita'
        verbose_name_plural="Listado de Citas"
    def __str__(self):
        return  f"Cita N°: {self.nro_cita}"


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
    ai_responsable_contrato = models.ForeignKey(Usuario, db_column='AI_Responsable_Contrato', on_delete=models.RESTRICT)  # Field name made lowercase.
    client_involucrado_contrato = models.ForeignKey(Usuario, db_column='Client_Involucrado_Contrato', on_delete=models.RESTRICT, related_name='client_contrato')  # Field name made lowercase.
    prop_involucrada_contrato = models.ForeignKey(Propiedad, db_column='Prop_Involucrada_Contrato', on_delete=models.CASCADE)  # Field name made lowercase.

    class Meta:
        db_table = 'contrato_cerrado'


class ContratoRutaDocumento(models.Model):
    id_contrato_ruta_documento = models.AutoField(db_column='ID_Contrato_Ruta_Documento', primary_key=True)
    nro_contrato_documento = models.ForeignKey(ContratoCerrado, db_column='NRO_Contrato_Documento', on_delete=models.CASCADE)  # Field name made lowercase.
    ruta_cd = models.CharField(db_column='Ruta_CD', max_length=100)  # Field name made lowercase.

    class Meta:
        db_table = 'contrato_ruta_documento'
        constraints = [models.UniqueConstraint(fields=['nro_contrato_documento', 'ruta_cd'], name='Contrato_Ruta_Documento_pk')]


class EmpleadoCobroPendiente(models.Model):
    TIPO_COBRO_EMPLEADO = (
        	('SU', 'Sueldo'),
        	('COM','Comision'),
    )
    nro_cobro = models.AutoField(db_column='NRO_Cobro', primary_key=True)  # Field name made lowercase.
    id_empleado_cobra = models.ForeignKey(Usuario, db_column='ID_Empleado_Cobra', on_delete=models.RESTRICT)  # Field name made lowercase.
    f_creacion_cobrop = models.DateField(db_column='F_Creacion_CobroP')  # Field name made lowercase.
    h_creacion_cobrop = models.TimeField(db_column='H_Creacion_CobroP')  # Field name made lowercase.
    monto_cobro_empleado = models.DecimalField(db_column='Monto_Cobro_Empleado', max_digits=10, decimal_places=0)  # Field name made lowercase.
    descripcion_cobro_empleado = models.CharField(db_column='Descripcion_Cobro_Empleado', max_length=100, blank=True, null=True)  # Field name made lowercase.
    tipo_cobro_empleado = models.CharField(choices=TIPO_COBRO_EMPLEADO, db_column='Tipo_Cobro_Empleado', max_length=8)  # Field name made lowercase.

    class Meta:
        db_table = 'empleado_cobro_pendiente'


class Caja(models.Model):
    id_caja = models.AutoField(db_column='ID_Caja', primary_key=True)  # Field name made lowercase.
    descripcion_caja = models.CharField(db_column='Descripcion_Caja', max_length=100)  # Field name made lowercase.
    isopen = models.BooleanField(db_column='IsOpen', default=False)  # Field name made lowercase. This field type is a guess.

    class Meta:
        db_table = 'caja'


class CierreCaja(models.Model):
    id_cierre_caja = models.AutoField(db_column='ID_Cierre_Caja', primary_key=True)
    id_caja_cierre = models.ForeignKey(Caja, db_column='ID_Caja_Cierre', on_delete=models.RESTRICT)  # Field name made lowercase.
    fecha_cierre_caja = models.DateField(db_column='Fecha_Cierre_Caja')  # Field name made lowercase.
    monto_cierre = models.DecimalField(db_column='Monto_Cierre', max_digits=10, decimal_places=0)  # Field name made lowercase.

    class Meta:
        db_table = 'cierre_caja'
        constraints = [models.UniqueConstraint(fields=['id_caja_cierre', 'fecha_cierre_caja'], name='CierreCaja_pk')]


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
    id_caja_transaccion = models.ForeignKey(Caja, db_column='ID_Caja_Transaccion', on_delete=models.RESTRICT)  # Field name made lowercase.
    cajera_responsable_transaccion = models.ForeignKey(Usuario, db_column='Cajera_Responsable_Transaccion', on_delete=models.RESTRICT, related_name='cajera_transac')  # Field name made lowercase.
    emp_cobra_transaccion = models.ForeignKey(Usuario, db_column='Emp_Cobra_Transaccion', blank=True, null=True, on_delete=models.RESTRICT, related_name='emp_transac')  # Field name made lowercase.
    client_paga_cobra_transaccion = models.ForeignKey(Usuario, db_column='Client_Paga-Cobra_Transaccion', blank=True, null=True, on_delete=models.RESTRICT)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    prop_involucrada_transaccion = models.ForeignKey(Propiedad, db_column='Prop_Involucrada_Transaccion', blank=True, null=True, on_delete=models.RESTRICT)  # Field name made lowercase.

    class Meta:
        db_table = 'transaccion'


class TransaccionRutaDocumento(models.Model):
    id_transaccion_ruta_documento = models.AutoField(db_column='ID_Transaccion_Ruta_Documento', primary_key=True)
    nro_transaccion_documento = models.ForeignKey(Transaccion, db_column='NRO_Transaccion_Documento', on_delete=models.CASCADE)  # Field name made lowercase.
    ruta_dt = models.CharField(db_column='Ruta_DT', max_length=100)  # Field name made lowercase.

    class Meta:
        db_table = 'transaccion_ruta_documento'
        constraints = [models.UniqueConstraint(fields=['nro_transaccion_documento', 'ruta_dt'], name='TransaccionRutaDocumento_pk')]


class DeudaCliente(models.Model):
    nro_deuda_cliente = models.AutoField(db_column='NRO_Deuda_Cliente', primary_key=True)  # Field name made lowercase.
    f_creacion_deuda = models.DateField(db_column='F_Creacion_Deuda')  # Field name made lowercase.
    monto_deuda = models.DecimalField(db_column='Monto_Deuda', max_digits=10, decimal_places=0)  # Field name made lowercase.
    id_cliente_debe = models.ForeignKey(Usuario, db_column='ID_Cliente_Debe', on_delete=models.RESTRICT)  # Field name made lowercase.
    id_propiedad_deuda = models.ForeignKey(Propiedad, db_column='ID_Propiedad_Deuda', on_delete=models.RESTRICT)  # Field name made lowercase.

    class Meta:
        db_table = 'deuda_cliente'


class CobroPendCliente(models.Model):
    nro_cobro_p_cliente = models.AutoField(db_column='NRO_Cobro_P_Cliente', primary_key=True)  # Field name made lowercase.
    f_creacion_cobro_pc = models.DateField(db_column='F_Creacion_Cobro_PC')  # Field name made lowercase.
    monto_cobro_pc = models.DecimalField(db_column='Monto_Cobro_PC', max_digits=10, decimal_places=0)  # Field name made lowercase.
    id_cliente_cobra = models.ForeignKey(Usuario, db_column='ID_Cliente_Cobra', on_delete=models.RESTRICT)  # Field name made lowercase.
    id_prop_involuc_cpc = models.ForeignKey(Propiedad, db_column='ID_Prop_Involuc_CPC', on_delete=models.RESTRICT)  # Field name made lowercase.

    class Meta:
        db_table = 'cobro_pend_cliente'


class RegistroDeCitas(models.Model):
    id_registro = models.AutoField(db_column='ID_Registro', primary_key=True)  # Field name made lowercase.
    nro_cita = models.PositiveIntegerField(db_column='NRO_Cita')  # Field name made lowercase.
    fechas_field = models.CharField(db_column='Fechas=>', max_length=8)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    fh_creacion = models.DateTimeField(db_column='FH_Creacion')  # Field name made lowercase.
    fh_asignacion = models.DateTimeField(db_column='FH_Asignacion')  # Field name made lowercase.
    fh_cita = models.DateTimeField(db_column='FH_Cita')  # Field name made lowercase.
    fh_conclusion = models.DateTimeField(db_column='FH_Conclusion')  # Field name made lowercase.
    secretaria_field = models.CharField(db_column='Secretaria=>', max_length=12)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    nombre_secretaria = models.CharField(db_column='Nombre_Secretaria', max_length=50)  # Field name made lowercase.
    apellido_secretaria = models.CharField(db_column='Apellido_Secretaria', max_length=50, blank=True, null=True)  # Field name made lowercase.
    dni_secretaria = models.CharField(db_column='DNI_Secretaria', max_length=20)  # Field name made lowercase.
    sexo_secretaria = models.CharField(db_column='Sexo_Secretaria', max_length=13, blank=True, null=True)  # Field name made lowercase.
    agente_inmobiliatio_field = models.CharField(db_column='Agente Inmobiliatio=>', max_length=21)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    nombre_ai = models.CharField(db_column='Nombre_AI', max_length=50)  # Field name made lowercase.
    apellido_ai = models.CharField(db_column='Apellido_AI', max_length=50, blank=True, null=True)  # Field name made lowercase.
    dni_ai = models.CharField(db_column='DNI_AI', max_length=20)  # Field name made lowercase.
    sexo_ai = models.CharField(db_column='Sexo_AI', max_length=13, blank=True, null=True)  # Field name made lowercase.
    cliente_field = models.CharField(db_column='Cliente=>', max_length=9)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    nombre_cliente = models.CharField(db_column='Nombre_Cliente', max_length=50)  # Field name made lowercase.
    apellido_cliente = models.CharField(db_column='Apellido_Cliente', max_length=50, blank=True, null=True)  # Field name made lowercase.
    dni_cliente = models.CharField(db_column='DNI_Cliente', max_length=20)  # Field name made lowercase.
    sexo_cliente = models.CharField(db_column='Sexo_Cliente', max_length=13, blank=True, null=True)  # Field name made lowercase.
    propiedad_field = models.CharField(db_column='Propiedad=>', max_length=11)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    ciudad_prop = models.CharField(db_column='Ciudad_Prop', max_length=20)  # Field name made lowercase.
    provincia_prop = models.CharField(db_column='Provincia_Prop', max_length=20)  # Field name made lowercase.
    pais_prop = models.CharField(db_column='Pais_Prop', max_length=20)  # Field name made lowercase.
    direccion_prop = models.CharField(db_column='Direccion_Prop', max_length=100)  # Field name made lowercase.
    tipo_prop = models.CharField(db_column='Tipo_Prop', max_length=12)  # Field name made lowercase.
    pisos_prop = models.PositiveIntegerField(db_column='Pisos_Prop')  # Field name made lowercase.
    metros_cuadrados_prop = models.DecimalField(db_column='Metros_Cuadrados_Prop', max_digits=10, decimal_places=0)  # Field name made lowercase.
    estado_prop = models.CharField(db_column='Estado_Prop', max_length=8)  # Field name made lowercase.
    dueño_field = models.CharField(db_column='Dueño=>', max_length=7)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    nombre_dueño = models.CharField(db_column='Nombre_Dueño', max_length=50)  # Field name made lowercase.
    apellido_dueño = models.CharField(db_column='Apellido_Dueño', max_length=50, blank=True, null=True)  # Field name made lowercase.
    dni_dueño = models.CharField(db_column='DNI_Dueño', max_length=20)  # Field name made lowercase.
    sexo_dueño = models.CharField(db_column='Sexo_Dueño', max_length=13, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'registro_de_citas'
