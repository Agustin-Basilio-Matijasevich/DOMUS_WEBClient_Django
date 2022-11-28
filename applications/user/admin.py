from django.contrib import admin
from .models import Usuario

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

admin.site.register(Usuario, UserAdmin)