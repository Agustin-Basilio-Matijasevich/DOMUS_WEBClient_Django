from django import forms
from django.contrib.auth import authenticate

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