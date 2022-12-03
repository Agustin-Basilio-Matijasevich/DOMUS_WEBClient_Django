import datetime
from django import forms
from django.contrib.auth import authenticate
from .models import Cita,Usuario
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget

TIPO_CITA = (
        	('SOL', 'Solicitud'),
        	('AG', 'Agendada'),
    )

class LoginUsuarioForm(forms.Form):
    username = forms.CharField(
        label='Usuario',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba su nombre usuario'
            }
        )
    )
    password = forms.CharField(
        label="Contraseña",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': "form-control",
                'placeholder': "Escriba aqui su contraseña"
            }
        )
    )
    
    def clean(self):
        cleaned_data = super(LoginUsuarioForm, self).clean()
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        
        if not authenticate(username=username, password=password):
            raise forms.ValidationError('Los datos del usuario no son correctos.')
    
        return self.cleaned_data

class DateInput(forms.DateInput):
    input_type = 'date'

class DateTime2(forms.DateInput):
    input_type = 'time'

class InputNumber(forms.DateInput):
    input_type= 'number'




class CitaForm(forms.Form):
    Cliente = forms.CharField(max_length=50, required=True)
    fecha = forms.DateField(widget=DateInput(attrs={
        'min': datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d'),
    }))
    hora= forms.TimeField(widget=DateTime2)
    Agente_Inmobiliario = forms.CharField(max_length=50, required=True)
    Codigo_de_Propiedad = forms.IntegerField()
    tipo_de_cita= forms.CharField(widget=forms.Select(choices=TIPO_CITA))

    def clean_agente(self):
        clienteForm = self.cleaned_data['Cliente']
        agenteForm = self.cleaned_data['Agente_Inmobiliario']
        agenteExist = Usuario.objects.get(nombres=agenteForm)

        if agenteExist:
            return agenteForm
        else:
            raise forms.ValidationError("No existe ningun agente inmboliario con ese nombre.")
        return agenteForm


class CitaAtendidaForm(forms.ModelForm):
    f_concluye_cita = forms.DateField(
        label='Fecha',
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                "type": "date",
                "required": "true",
                "min": datetime.datetime.now().strftime('%Y-%m-%d'),
            }),
            input_formats=('%Y-%m-%d',),
    )
    h = forms.TimeField(
        label='Hora',
        widget=forms.TimeInput(
            format='%H:%M',
            attrs={
                'type': 'time',
                'required': 'true'
            }),
            input_formats=('%H:%M',),
    )
    class Meta:
        model= Cita
        fields = (
            'f_concluye_cita',
            'h_concluye_cita',
        )


class CitaUpdateForm(forms.ModelForm):
    f_cita = forms.DateField(
        label='Fecha',
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                "type": "date",
                "required": "true",
                "min": datetime.datetime.now().strftime('%Y-%m-%d'),
            }),
            input_formats=('%Y-%m-%d',),
    )
    h_cita = forms.TimeField(
        label='Hora',
        widget=forms.TimeInput(
            format='%H:%M',
            attrs={
                'type': 'time',
                'required': 'true'
            }),
            input_formats=('%H:%M',),
    )
    
    class Meta:
        model = Cita
        fields = (
            'client_solicita_cita',
            'f_cita',
            'h_cita',
            'ai_atiende_cita',
            'propiedad_involucrada',
            'tipo_cita',
        )
    


        
        



