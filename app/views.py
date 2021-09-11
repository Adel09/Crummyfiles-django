from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .models import File, Link
import uuid


# Create your views here.

def home(request):
    user = request.user
    context = {'title' : "Home | Crummy Files",
                'user' : user}
    return render(request, 'index.html', context)


def signupuser(request):

    if request.method == 'GET':
        context = {'title': 'Create your account | Crummy Files'}
        return render(request, 'signup.html', context)
    else:
        if request.POST['pass1'] == request.POST['pass2']:
            try:
                user = User.objects.create_user(email=request.POST['email'],username=request.POST['username'], password=request.POST['pass1'], first_name=request.POST['fname'], last_name=request.POST['lname'])
                user.save()
                login(request, user)
                return redirect('dashboard')
            except IntegrityError:
                context = {'title': 'Create your account| Crummy Files',
                            'error' : 'User already registered'}
                return render(request, 'signup.html', context)
        else:
            context = {'title': 'Create your account| Crummy files',
                            'error' : 'Passwords do not match'}
            return render(request, 'signup.html', context)

def signinuser(request):
    if request.method == 'GET':
        context = {'title' : "Log into your dashboard"}
        return render(request, 'login.html', context)
        
    else:
        email = request.POST['email']
        password = request.POST['pass']
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            context = {'title': 'Log into your dashboard| Crummy files',
                            'error' : 'Invalid user'}
            return render(request, 'signup.html', context)


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def dashboard(request):
    user = User.objects.get(username=request.user)
    files = File.objects.filter(owner = user)
    name = user.first_name
    context = {'title': 'My Files | Crummy Files',
                    'name': name,
                    'user': user,
                    'files' : files}
    return render(request, 'dashboard.html', context)


def upload(request):
    if request.method == 'GET':
        user = User.objects.get(username=request.user)
        context = {'title': 'Upload File | Crummy Files',
                        'user': user}
        return render(request, 'upload.html', context)
    else:
        name = request.POST['name']
        desc = request.POST['desc']
        file = request.FILES['file']
        owner = request.user

        file = File.objects.create(id= str(uuid.uuid4())[:5], name=name, description=desc, file=file, owner=owner)
        file.save()

        # link = Link.objects.create(uuid= str(uuid.uuid4())[:5], file=file)
        # link.save()

        return redirect('dashboard')

        
def getfile(request, id):
    # file = File.objects.get(id=id)
    file = get_object_or_404(File, id=id)
    context = {'title': 'Upload File | Crummy Files',
                        'file': file}
    return render(request, 'downloadfile.html', context)


def delete(request, id):
    file = File.objects.get(id=id)
    if request.method == 'POST':
        if file.owner == request.user:
            file.delete()
            return redirect('dashboard')




