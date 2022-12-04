import datetime
from django import forms
from django.contrib.auth import authenticate
from .models import Cita,Usuario
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget
from django.contrib import messages

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
            raise forms.ValidationError("Usuario y/o contraseña incorrecta.")

        return self.cleaned_data

class CitaAgendadaForm(forms.ModelForm):
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
        )

class CitaSolicitudForm(forms.ModelForm):
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
