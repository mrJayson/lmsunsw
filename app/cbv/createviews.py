
from django.views.generic import View, CreateView
from app.forms import CreateUserForm
from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class CreateUser(CreateView):
    template_name = 'app/create_user.html'
    form_class = CreateUserForm

    def get_success_url(self):
        return reverse('alert', kwargs={'tag':'create_user_success'})
