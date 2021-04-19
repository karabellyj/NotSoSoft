from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView


class UserRegistrationView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(reverse_lazy('project-list'))
