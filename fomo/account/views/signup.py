from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.contrib.auth import authenticate, login
from django_mako_plus import view_function
from .. import dmp_render, dmp_render_to_string

from formlib.form import FormMixIn
from account import models as amod
from catalog.models import ShoppingCart

@view_function
def process_request(request):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/account/index')

        user = amod.FomoUser()
        form = CreateUserForm(request, user=user)

        if form.is_valid():
            form.commit(user)
            return HttpResponseRedirect('/homepage/index/')

        context = {
            'form': form,
            'title': 'Sign-up',
        }
        return dmp_render(request, 'signup.html', context)


class CreateUserForm(FormMixIn, forms.Form):

    def init(self, user):
        self.fields['first_name'] = forms.CharField(label='First Name', max_length=30)
        self.fields['last_name'] = forms.CharField(label='Last Name', max_length=30)
        self.fields['username'] = forms.CharField(label='Username', max_length=150)
        self.fields['email'] = forms.CharField(label='Email', max_length=30)
        self.fields['password'] = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput())
        self.fields['birthday'] = forms.DateTimeField(label='Birthday')
        self.fields['phone'] = forms.CharField(label='Phone Number', max_length=20)
        self.fields['address'] = forms.CharField(label='Street Address', max_length=200)
        self.fields['city'] = forms.CharField(label='City', max_length=50)
        self.fields['state'] = forms.CharField(label='State', max_length=50)
        self.fields['zipcode'] = forms.CharField(label='Zipcode', max_length=50)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        users = amod.FomoUser.objects.filter(username=username)
        if len(users) > 0:
             raise forms.ValidationError('Sorry, this username is already taken')
        return username

    def commit(self, user):
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.username = self.cleaned_data.get('username')
        user.email = self.cleaned_data.get('email')
        user.set_password(self.cleaned_data.get('password'))
        user.birthday = self.cleaned_data.get('birthday')
        user.phone = self.cleaned_data.get('phone')
        user.address = self.cleaned_data.get('address')
        user.city = self.cleaned_data.get('city')
        user.state = self.cleaned_data.get('state')
        user.zipcode = self.cleaned_data.get('zipcode')
        user.save()
        cart = ShoppingCart(user=user)
        cart.save()
