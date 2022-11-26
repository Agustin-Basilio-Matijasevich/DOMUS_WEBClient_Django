from django.urls import path
from .views import CitasView

urlpatterns = [
    path(
        'citas/',
        CitasView.as_view(),
        name='citas',
    ),
]