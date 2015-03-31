
from django.views.generic import View, CreateView
from app.forms import CreateUserForm
from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class CreateUser(CreateView):
    template_name = 'create_user.html'
    form_class = CreateUserForm

    def get_success_url(self):
        return reverse('alert', kwargs={'tag':'create_user_success'})




    '''def get(self, request):
        register_user_form = CreateUserForm()
        self.extra_context.update({'register_user_form':register_user_form})


        return render(request, self.template, context_instance = RequestContext(request, self.extra_context))

    def post(self, request):
        register_user_form = RegisterUserForm(request.POST)
        self.extra_context.update({'register_user_form':register_user_form})

        if register_user_form.is_valid():
            register_user_form.save()
            # display confirmation page once successful
            self.extra_context.update({'success':True})
        else:
            # if error occurs, render the registration page again
            print register_user_form.errors

        return render(request, self.template, context_instance = RequestContext(request, self.extra_context))
        '''