from django.conf import settings
from django.http import HttpResponseRedirect
from django_mako_plus import view_function
from django.contrib.auth import authenticate, login
from django import forms

from .. import dmp_render, dmp_render_to_string

from formlib.form import FormMixIn
from account import models as amod

@view_function
def process_request(request):

    user = amod.FomoUser()
    form = LoginForm(request, user=user)

    if form.is_valid():
        form.commit(user)
        user = authenticate(username=user.username, password=user.password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/homepage/index/')

    context = {
        'user' : user,
        'form': form,
        'title': 'Edit User',
    }
    # if not authenticated
    return dmp_render(request, 'login.html', context)

class LoginForm(FormMixIn, forms.Form):

    def init(self, user):
        self.fields['username'] = forms.CharField(label='Username', max_length=150)
        self.fields['password'] = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput())

    def commit(self, user):
        user.username = self.cleaned_data.get('username')
        user.password = self.cleaned_data.get('password')
