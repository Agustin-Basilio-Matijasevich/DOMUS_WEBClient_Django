from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, CreateView, View
from django.views.generic.edit import FormView
from .forms import LoginUsuarioForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin


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
        return super(LoginUsuarioView, self).form_valid(form)

class CerrarSesionView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(
            reverse('login')
        )