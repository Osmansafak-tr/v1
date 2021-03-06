from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy


from .forms import CustomUserCreationForm
# Create your views here.
class SignupView(CreateView):
    template_name = 'signup.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')