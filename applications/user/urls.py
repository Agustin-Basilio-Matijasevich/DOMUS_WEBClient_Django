from django.urls import path
from .views import HomeView,LoginUsuarioView, CerrarSesionView

urlpatterns = [
    path(
        '',
        HomeView.as_view(),
        name = 'home'
    ),
    path(
        'login/',
        LoginUsuarioView.as_view(),
        name= 'login'
    ),
    path(
        'logout/',
        CerrarSesionView.as_view(),
        name= 'logout'
    ),
]