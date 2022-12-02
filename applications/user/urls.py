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
        name= 'solicitud'
    ),
    path(
        'modificarCita/<nro_cita>/',
        views.modificarCita,
        name= 'modificarCita'
    ),
    path(
        'eliminarCita/<nro_cita>/',
        views.eliminarCita,
        name= 'eliminarCita'
    ),
    path(
        'buscarCita/<date>/',
        views.buscarFecha,
        name= 'agenda'
    ),
]