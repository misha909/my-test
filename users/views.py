from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest

from users.models import CustomUser
from users.forms import CustomUserForm, UserForm
from django.contrib.auth.models import User

from django import forms
from django.template import RequestContext
import django_excel as excel

def user_list(request):
    try:
        users = CustomUser.objects.all()
    except users.DoesNotExist:
        raise Http404('user does not exist.')

    context = { 'users' : users }

    return render(request, 'users/index.html', context)

def add_user(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        custom_user_form = CustomUserForm(data=request.POST)

        if user_form.is_valid() and custom_user_form.is_valid():
            user = user_form.save()
            customer = custom_user_form.save(commit=False)
            customer.user = user
            customer.save()

            return HttpResponseRedirect('/users/')
        else:
            context = {
                'user_form_errors': user_form.errors,
                'custom_user_form_errors': custom_user_form.errors
            }

            return render(request, 'users/add_user.html', context)
    
    return render(request, 'users/add_user.html')

from datetime import datetime

def edit_user(request, user_id=None):
    if user_id is None:
        return HttpResponseRedirect('/users/')

    user = User.objects.get(id=user_id)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        birthday = request.POST.get('birthday')
        try:
            custom_user = CustomUser.objects.get(user=user)
            custom_user.birthday=birthday
            custom_user.save(update_fields=['birthday'])
            user.username=username
            user.save(update_fields=['username'])
        except AttributeError:
            pass

        return HttpResponseRedirect('/users/')
            
    custom_user = CustomUser.objects.get(user=user)
    context = {
        'user': user,
        'custom_user': custom_user}
    return render(request, 'users/edit_user.html', context)

def delete_user(request, user_id=None):
    if user_id is None:
        return HttpResponseRedirect('/users/')
    
    user = User.objects.get(id=user_id)
    CustomUser.objects.get(user=user).delete()
    user.delete()

    return HttpResponseRedirect('/users/')

class UploadFileForm(forms.Form):
    file = forms.FileField()

def upload(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            filehandle = request.FILES['file']
            return excel.make_response(filehandle.get_sheet(), "csv")
        else:
            return HttpResponseBadRequest()
    else:
        form = UploadFileForm()
    return render_to_response('index.html',
                              {'form': form},
                              context_instance=RequestContext(request))

def download(request):
    sheet = excel.pe.Sheet([[1, 2],[3, 4]])
    return excel.make_response(sheet, "csv")    