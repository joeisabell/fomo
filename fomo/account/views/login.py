from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django import forms

from django_mako_plus import view_function
from .. import dmp_render, dmp_render_to_string

from formlib.form import FormMixIn
from account import models as amod

@view_function
def process_request(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect('/account/index')

    form = LoginForm(request)

    if form.is_valid():
        # set redirect_url to home index page if the a next urlparam doesn't exist
        redirect_url = request.GET.get('next')
        if redirect_url is None: redirect_url = '/homepage/index'
        return HttpResponseRedirect(redirect_url)

    context = {
        'form': form,
        'title': 'Login',
    }

    # if not authenticated
    return dmp_render(request, 'login.html', context)

class LoginForm(FormMixIn, forms.Form):

    def init(self, user):
        self.fields['username'] = forms.CharField(label='Username', max_length=150)
        self.fields['password'] = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput())

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        auth_user = authenticate(username=username, password=password)
        if auth_user is not None:
            login(self.request, auth_user)
        else:
            raise forms.ValidationError('Incorrect password.')

        return self.cleaned_data

    def commit(self):
        pass
