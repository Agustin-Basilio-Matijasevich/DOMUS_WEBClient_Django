import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, CreateView, View
from django.views.generic.edit import FormView
from .forms import LoginUsuarioForm, CitaUpdateForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Cita, Usuario, Propiedad


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'
    login_url= reverse_lazy('login')

class LoginUsuarioView(FormView):
    template_name = 'login.html'
    form_class= LoginUsuarioForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = authenticate(
            username= form.cleaned_data['username'],
            password= form.cleaned_data['password'],
        )
        login(self.request, user)
        messages.success(self.request, 'Usuario logueado con exito')
        return super(LoginUsuarioView, self).form_valid(form)

class CerrarSesionView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(
            reverse('login')
        )


def CitaList(request):
    citas = Cita.objects.filter(tipo_cita='SOL')
    data = {
        'citas': citas
    }
    return render(request, 'citas.html', data)


def agregarCita(request):
    data = {
            'form': CitaUpdateForm()
        }
    
    if request.method=='POST':
        
        formulario = CitaUpdateForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Cita agendada con exito')
            return redirect(to='solicitud')
        else:
            data["form"] = formulario
            messages.error(request,"Error al crear cita.")
    
    return render(request,'agregarCita.html', data)

def modificarCita(request, nro_cita):
    cita = get_object_or_404(Cita, nro_cita=nro_cita)

    data = {
        'form': CitaUpdateForm(instance=cita)
    }
    if request.method == 'POST':
        formulario = CitaUpdateForm(data=request.POST, instance=cita, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Cita modificada con exito')
            return redirect(to='solicitud')
        data['form'] = formulario

    return render(request, 'editarCita.html', data)

def eliminarCita(request, nro_cita):
    cita = get_object_or_404(Cita, nro_cita=nro_cita)
    cita.delete()
    messages.success(request, 'Solicitud de cita eliminada con exito')
    return HttpResponseRedirect(
            reverse('solicitud')
        )

def buscarFecha(request, date):
    cita = Cita.objects.filter(f_cita=date)
    print(cita)
    if cita:
        data = {
        'form': cita,
        }
    else:
        messages.error(request,"No se encontraron citas para la fecha indicada.")
        return redirect(to='agenda')
    
    return render(request, 'agenda.html', data)
    





    

    