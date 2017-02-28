from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django_mako_plus import view_function
from .. import dmp_render, dmp_render_to_string

from formlib.form import FormMixIn
from account import models as amod

@view_function
@login_required
def process_request(request):

    try:
        user = request.user
    except amod.FomoUser.DoesNotExist:
        return HttpResponseRedirect('/account/login')

    # process the form
    form = EditUserForm(request, user=user, initial={
        'first_name' : user.first_name,
        'last_name' : user.last_name,
        'username' : user.username,
        'email' : user.email,
        'birthday' : user.birthday,
        'phone' : user.phone,
        'address' : user.address,
        'city' : user.city,
        'state' : user.state,
        'zipcode' : user.zipcode,
    })

    if form.is_valid():
        form.commit(user)
        return HttpResponseRedirect('/account/index/')

    context = {
        'user' : user,
        'form': form,
        'title': 'Edit Account Information',
    }
    return dmp_render(request, 'edit.html', context)



class EditUserForm(FormMixIn, forms.Form):

    def init(self, user):

        self.fields['first_name'] = forms.CharField(label='First Name', max_length=30)
        self.fields['last_name'] = forms.CharField(label='Last Name', max_length=30)
        self.fields['username'] = forms.CharField(label='Username', max_length=150)
        self.fields['email'] = forms.CharField(label='Email', max_length=30)
        self.fields['birthday'] = forms.DateTimeField(label='Birthday')
        self.fields['phone'] = forms.CharField(label='Phone Number', max_length=20)
        self.fields['address'] = forms.CharField(label='Street Address', max_length=200)
        self.fields['city'] = forms.CharField(label='City', max_length=50)
        self.fields['state'] = forms.CharField(label='State', max_length=50)
        self.fields['zipcode'] = forms.CharField(label='Zipcode', max_length=50)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        users = amod.FomoUser.objects.filter(username=username).exclude(id=self.request.user.id)
        if len(users) > 0:
             raise forms.ValidationError('Sorry, this username is already taken')
        return username

    def commit(self, user):
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.username = self.cleaned_data.get('username')
        user.email = self.cleaned_data.get('email')
        user.birthday = self.cleaned_data.get('birthday')
        user.phone = self.cleaned_data.get('phone')
        user.address = self.cleaned_data.get('address')
        user.city = self.cleaned_data.get('city')
        user.state = self.cleaned_data.get('state')
        user.zipcode = self.cleaned_data.get('zipcode')
        user.save()

###################################################
## Change Password

@view_function
@login_required
def password(request):

        # process the form
        form = ChangeUserPasswordForm(request)

        if form.is_valid():
            form.commit(request.user)
            return HttpResponseRedirect('/account/index/')

        context = {
            'form': form,
            'title': 'Change Password',
        }
        return dmp_render(request, 'edit.html', context)


class ChangeUserPasswordForm(FormMixIn, forms.Form):

    def init(self):
        self.fields['password'] = forms.CharField(label='Old Password', max_length=100, widget=forms.PasswordInput())
        self.fields['new_password'] = forms.CharField(label='New Password', max_length=100, widget=forms.PasswordInput())
        self.fields['confirm_password'] = forms.CharField(label='Confirm New Password', max_length=100, widget=forms.PasswordInput())

    def clean(self):
        old_password = self.cleaned_data.get('password')
        new_password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if new_password != confirm_password:
            raise forms.ValidationError("Passwords don't match.")

        auth_user = authenticate(username=self.request.user.username, password=self.cleaned_data.get('password'))
        if auth_user is None:
            raise forms.ValidationError('Incorrect password.')

        return self.cleaned_data

    def commit(self, user):
        user.set_password(self.cleaned_data.get('new_password'))
        user.save()

        # log user back in
        auth_user = authenticate(username=self.request.user.username, password=self.cleaned_data.get('new_password'))
        login(self.request, auth_user)
