import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, CreateView, View
from django.views.generic.edit import FormView
from .forms import LoginUsuarioForm, CitaSolicitudForm, CitaAgendadaForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Cita, Usuario, Propiedad, PropiedadRutaDocumento
from django.core.paginator import Paginator
from django.http import Http404


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


#Funcionalidad para el rol de Secretario. DOMUS 2.0

#Vista que se encarga de listar todas aquellas vistas las cuales se categorizan por ser de 'solicitud'
def CitaList(request):
    citas = Cita.objects.filter(tipo_cita='SOL')
    data = {
        'citas': citas
    }
    return render(request, 'secretario/solicitudCita.html', data)

#Vista encargada de agregar una nueva cita.(Ya sea de solicitud o agendada)
def agregarCita(request):
    data = {
            'form': CitaAgendadaForm()
        }

    if request.method=='POST':

        formulario = CitaAgendadaForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            cita = formulario.save(commit=False)
            fecha = cita.f_cita
            hora = cita.h_cita

            secretario = Usuario.objects.get(id=request.user.id)
            print(request.user)
            cita.secre_asigna_cita = secretario
            cita.tipo_cita = 'AG'
            cita.f_creacion_cita = fecha
            cita.h_creacion_cita = hora
            cita.f_asignacion_cita = fecha
            cita.h_asignacion_cita = hora
            cita.save()
            messages.success(request, 'Cita agendada con exito')
            return redirect(to='agendaSecretario')
        else:
            data["form"] = formulario
            messages.error(request,"Error al crear cita.")

    return render(request,'secretario/agregarCita.html', data)

#Vista encargada de modificar una solicitud de cita.
def modificarCitaSolicitud(request, nro_cita):
    cita = get_object_or_404(Cita, nro_cita=nro_cita)

    data = {
        'form': CitaSolicitudForm(instance=cita)
    }
    if request.method == 'POST':
        formulario = CitaSolicitudForm(data=request.POST, instance=cita, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Cita agendada con exito')
            return redirect(to='solicitudCita')
        data['form'] = formulario
    return render(request, 'secretario/editarCitaSolicitud.html', data)

#Vista que se encarga de modificar una cita que ya fue agendadas
def modificarCitaAgendada(request, nro_cita):
    cita = get_object_or_404(Cita, nro_cita=nro_cita)

    data = {
        'form': CitaAgendadaForm(instance=cita)
    }
    if request.method == 'POST':
        formulario = CitaAgendadaForm(data=request.POST, instance=cita, files=request.FILES)
        if formulario.is_valid():
            cita = formulario.save(commit=False)
            cita.tipo_cita = 'AG'
            cita.save()
            messages.success(request, 'Cita modificada con exito')
            return redirect(to='agendaSecretario')
        data['form'] = formulario

    return render(request, 'secretario/editarCitaAgendada.html', data)

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
            reverse('agendaSecretario')
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

        return render(request, 'secretario/agenda.html', data)

#Vista que carga todas aquellas citas las cuales fueron agendadas.
def agenda(request):
    if request.method=='GET':
        citas = Cita.objects.filter(tipo_cita='AG')

        data = {
            'citas': citas,
            'datetime': datetime.datetime.now()
        }
        return render(request, 'secretario/agenda.html', data)



#Funcionalidad para el rol de Agente inmobiliario:

class HomeInmobiliaria(TemplateView):
    template_name = 'agenteinmobiliario/agenda.html'

#Filtramos todas las citas disponibles para ese agente.
def citasDisponiblesInmobiliaria(request):
    if request.method == 'GET':
        citas = Cita.objects.filter(
        tipo_cita='AG',
        f_concluye_cita = None,
        h_concluye_cita= None,
        ai_atiende_cita= request.user,
        )

        data = {
            'citas': citas
        }
    return render(request, 'agenteInmobiliario/agenda.html', data)

#Filtramos por fecha, todas aquellas citas que coincidan
def filtrarCitasInmobiliaria(request):
    if request.method == 'GET':
        citas = Cita.objects.filter(
        tipo_cita='AG',
        f_concluye_cita = None,
        h_concluye_cita= None,
        ai_atiende_cita= request.user,
        f_cita = request.GET['date'],
        )

        data = {
            'citas': citas
        }

    return render(request, 'agenteInmobiliario/agenda.html', data)

def atenderCitaAgendada(request, nro_cita):
    cita = get_object_or_404(Cita, nro_cita=nro_cita)

    cita.f_concluye_cita= datetime.date.today()
    cita.h_concluye_cita= datetime.datetime.now().strftime('%H:%M')
    cita.save()

    messages.success(request, 'Cita atendida con exito')

    return render(request, 'agenteInmobiliario/agenda.html')


class CatalogoPropiedadesAgente(ListView):
    template_name = 'agenteInmobiliario/propiedades.html'
    queryset = PropiedadRutaDocumento.objects.all()
    context_object_name = 'propiedades'
    paginate_by = 5
