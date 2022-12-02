import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, CreateView, View
from django.views.generic.edit import FormView
from .forms import LoginUsuarioForm, CitaUpdateForm, CitaForm
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

#Vista que se encarga de listar todas aquellas vistas las cuales se categorizan por ser de 'solicitud'
def CitaList(request):
    citas = Cita.objects.filter(tipo_cita='SOL')
    data = {
        'citas': citas
    }
    return render(request, 'SolicitudCita.html', data)

#Vista encargada de agregar una nueva cita.(Ya sea de solicitud o agendada)
def agregarCita(request):
    data = {
            'form': CitaUpdateForm()
        }
    
    if request.method=='POST':
        
        formulario = CitaUpdateForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Cita agendada con exito')
            return redirect(to='solicitudCita')
        else:
            data["form"] = formulario
            messages.error(request,"Error al crear cita.")
    
    return render(request,'agregarCita.html', data)

#Vista encargada de modificar una solicitud de cita.
def modificarCitaSolicitud(request, nro_cita):
    cita = get_object_or_404(Cita, nro_cita=nro_cita)

    data = {
        'form': CitaUpdateForm(instance=cita)
    }
    if request.method == 'POST':
        formulario = CitaUpdateForm(data=request.POST, instance=cita, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Cita modificada con exito')
            return redirect(to='solicitudCita')
        data['form'] = formulario
    return render(request, 'editarCitaSolicitud.html', data)

#Vista que se encarga de modificar una cita que ya fue agendadas
def modificarCitaAgendada(request, nro_cita):
    cita = get_object_or_404(Cita, nro_cita=nro_cita)

    data = {
        'form': CitaUpdateForm(instance=cita)
    }
    if request.method == 'POST':
        formulario = CitaUpdateForm(data=request.POST, instance=cita, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Cita modificada con exito')
            return redirect(to='agenda')
        data['form'] = formulario

    return render(request, 'editarCitaAgendada.html', data)

#Vista encargada de eliminar una solicitud de cita. Retorna a la lista de solicitudes.
def eliminarCitaSolicitud(request, nro_cita):
    cita = get_object_or_404(Cita, nro_cita=nro_cita)
    cita.delete()
    messages.success(request, 'Solicitud de cita eliminada con exito')
    return HttpResponseRedirect(
            reverse('solicitudCita')
        )

#Vista encargada de eliminar una cita agendada. Retorna a la agenda.
def eliminarCitaAgendada(request, nro_cita):
    cita = get_object_or_404(Cita, nro_cita=nro_cita)
    cita.delete()
    messages.success(request, 'Solicitud de cita eliminada con exito')
    return HttpResponseRedirect(
            reverse('agenda')
        )

#Vista que busca todas aquellas citas que cumpla con la fecha que recibimos por GET.
def buscarFecha(request):
    if request.method=='GET':
        citas = Cita.objects.filter(f_cita=request.GET['date'])
        data = {
            'datetime' : datetime.datetime.now()
        }
        if citas:
            data['citas'] = citas
        else:
            messages.error(request,"No se encontraron citas para la fecha indicada.")

        return render(request, 'agenda.html', data)

#Vista que carga todas aquellas citas las cuales fueron agendadas.
def agenda(request):
    if request.method=='GET':
        citas = Cita.objects.filter(tipo_cita='AG')
        
        data = {
            'citas': citas,
            'datetime': datetime.datetime.now()
        }
        return render(request, 'agenda.html', data)
        
    





    

    