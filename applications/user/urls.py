from django.urls import path
from . import views

urlpatterns = [
    path(
        '',
        views.HomeView.as_view(),
        name = 'home'
    ),
    path(
        'login/',
        views.LoginUsuarioView.as_view(),
        name= 'login'
    ),
    path(
        'logout/',
        views.CerrarSesionView.as_view(),
        name= 'logout'
    ),
    path(
        'agendarCita/',
        views.agregarCita,
        name= 'agendarCita'
    ),
    path(
        'solicitudCitas/',
        views.CitaList,
        name= 'solicitudCita'
    ),
    path(
        'modificarCitaSolicitud/<nro_cita>/',
        views.modificarCitaSolicitud,
        name= 'modificarCitaSolicitud'
    ),
    path(
        'modificarCitaAgendada/<nro_cita>/',
        views.modificarCitaAgendada,
        name= 'modificarCitaAgendada'
    ),
    path(
        'eliminarCitaSolicitud/<nro_cita>/',
        views.eliminarCitaSolicitud,
        name= 'eliminarCitaSolicitud'
    ),
    path(
        'eliminarCitaAgendada/<nro_cita>/',
        views.eliminarCitaAgendada,
        name= 'eliminarCitaAgendada'
    ),
    path(
        'buscarCita',
        views.buscarFecha,
        name= 'buscarCita'
    ),
    path(
        'agenda/',
        views.agenda,
        name= 'agendaSecretario'
    ),
    path(
        'agendaInmobiliaria/',
        views.citasDisponiblesInmobiliaria,
        name= 'agendaInmobiliaria'
    ),
    path(
        'buscarCitaInmobiliaria/',
        views.filtrarCitasInmobiliaria,
        name= 'filtrarCitasInmobiliaria'
    ),
    path(
        'atenderCitaAgendada/<nro_cita>/',
        views.atenderCitaAgendada,
        name= 'atenderCitaAgendada'
    ),
    path(
        'catalogoPropiedades/',
        views.CatalogoPropiedadesAgente.as_view(),
        name= 'catalogoPropiedades'
    ),
]
