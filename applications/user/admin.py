from django.contrib import admin
from .models import Usuario, Cita, Propiedad, Ciudad, Provincia, Pais, PropiedadRutaDocumento

admin.site.site_header = 'DOMUS 2.0 Alpha'

admin.site.index_title = 'Administracion'

admin.site.site_title = 'DOMUS'

class UserAdmin(admin.ModelAdmin):

    list_display = ('username', 'nombres', 'tipo_usuario', 'is_superuser', 'is_staff')

    search_fields =  ('username', 'nombres', 'apellidos', 'dni_cuil', 'email')

    ordering = ('-is_superuser', '-is_staff', 'username',)

    def save_model(self, request, obj, form, change):
        if obj.password.startswith('pbkdf2'):
            obj.password=obj.password
        else:
            obj.set_password(obj.password) 
        super().save_model(request, obj, form, change)

class PropiedadAdmin(admin.ModelAdmin):
    list_display = (Propiedad.CodProp, 'tipo_propiedad', 'estado_propiedad', 'direccion', 'precio_sugerido', Propiedad.Dueño, Propiedad.Ubicacion, Propiedad.is_Disponible)
    search_fields = ('direccion', Propiedad.Ubicacion, Propiedad.Dueño)
    list_filter = ('tipo_propiedad', 'estado_propiedad')
    ordering = ('tipo_propiedad', 'estado_propiedad')

admin.site.register(Usuario, UserAdmin)
admin.site.register(Cita)
admin.site.register(Propiedad, PropiedadAdmin)
admin.site.register(PropiedadRutaDocumento)
admin.site.register(Ciudad)
admin.site.register(Provincia)
admin.site.register(Pais)