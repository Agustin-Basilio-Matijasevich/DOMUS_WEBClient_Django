from django.shortcuts import render
from django.views.generic import TemplateView

class CitasView(TemplateView):
    template_name = "citas.html"
