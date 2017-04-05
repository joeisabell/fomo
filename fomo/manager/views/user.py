from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.decorators import login_required, permission_required
from django_mako_plus import view_function
from .. import dmp_render, dmp_render_to_string

from formlib.form import FormMixIn
from account import models as amod

@view_function
@login_required
@permission_required('account.change_fomouser', raise_exception=True)
def process_request(request):

    try:
        user = amod.FomoUser.objects.get(id=request.urlparams[0])
    except amod.FomoUser.DoesNotExist:
        return HttpResponseRedirect('/manager/users')

    user_groups = {}
    for p in user.groups.all():
        user_groups[p.id] = p

    user_permissions = {}
    for p in user.user_permissions.all():
        user_permissions[p.id] = p

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
        'groups' : user_groups,
        'permissions' : user_permissions,
    })

    if form.is_valid():
        form.commit(user)
        return HttpResponseRedirect('/manager/users/')

    context = {
        'user' : user,
        'form': form,
        'title': 'Edit User',
    }
    return dmp_render(request, 'user.html', context)


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
        self.fields['groups'] = forms.ModelMultipleChoiceField(label='Groups', queryset=Group.objects.all())
        self.fields['permissions'] = forms.ModelMultipleChoiceField(label='User Permissions', queryset=Permission.objects.all())

    def clean_username(self):
        username = self.cleaned_data.get('username')
        users = amod.FomoUser.objects.filter(username=username).exclude(id=self.request.urlparams[0])
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
        user.groups.clear()
        user.user_permissions.clear()
        for group in self.cleaned_data.get('groups'):
            user.groups.add(group)
        for perm in self.cleaned_data.get('permissions'):
            user.user_permissions.add(perm)
            user.save()


###################################################
## Delete Users

@view_function
@login_required
@permission_required('account.delete_fomouser', raise_exception=True)
def delete(request):
    try:
        user = amod.FomoUser.objects.get(id=request.urlparams[0])
    except amod.FomoUser.DoesNotExist:
        return HttpResponseRedirect('/manager/users')

    user.delete()
    return HttpResponseRedirect('/manager/users')


###################################################
## Create Users

@view_function
@login_required
@permission_required('account.add_fomouser', raise_exception=True)
def create(request):
        user = amod.FomoUser()
        # process the form
        form = CreateUserForm(request, user=user)

        if form.is_valid():
            print('>>> form is valid')
            form.commit(user)
            return HttpResponseRedirect('/manager/users/')

        context = {
            'user' : user,
            'form': form,
            'title': 'Create a New User',
        }
        return dmp_render(request, 'user.html', context)


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
        self.fields['groups'] = forms.ModelMultipleChoiceField(label='Groups', queryset=Group.objects.all())
        self.fields['permissions'] = forms.ModelMultipleChoiceField(label='User Permissions', queryset=Permission.objects.all())

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
        for group in self.cleaned_data.get('groups'):
            user.groups.add(group)
        for perm in self.cleaned_data.get('permissions'):
            user.user_permissions.add(perm)


###################################################
## Change User Password

@view_function
@login_required
@permission_required('account.change_fomouser', raise_exception=True)
def change_password(request):

        try:
            user = amod.FomoUser.objects.get(id=request.urlparams[0])
        except amod.FomoUser.DoesNotExist:
            return HttpResponseRedirect('/manager/users')

        # process the form
        form = ChangeUserPasswordForm(request, user=user, initial={
            'username' : user.username,
        })

        if form.is_valid():
            print('>>> form is valid')
            form.commit(user)
            return HttpResponseRedirect('/manager/users/')

        context = {
            'user' : user,
            'form': form,
            'title': 'Change Password',
        }
        return dmp_render(request, 'user.html', context)


class ChangeUserPasswordForm(FormMixIn, forms.Form):

    def init(self, user):
        self.fields['username'] = forms.CharField(label='Username', disabled=True, max_length=150)
        self.fields['password'] = forms.CharField(label='New Password', max_length=100, widget=forms.PasswordInput())
        self.fields['confirm_password'] = forms.CharField(label='Confirm New Password', max_length=100, widget=forms.PasswordInput())

    def clean(self):

        new_password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if new_password != confirm_password:
            raise forms.ValidationError("Passwords don't match.")

        return self.cleaned_data

    def commit(self, user):
        user.set_password(self.cleaned_data.get('password'))
        user.save()
