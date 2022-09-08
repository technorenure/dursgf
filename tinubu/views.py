from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User,Group
from django.contrib import messages
from .forms import CreateUserForm, SupportGroupForm
from .models import SupportGroup, LocalGovt, GroupType, Team, Profile, Registered

from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only_url


def home(request):
    teams = Team.objects.all()
    users = SupportGroup.objects.all().count()
    context = {
        'teams': teams,
    }
    return render(request, 'index.html', context )
 
@unauthenticated_user
def create_user(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
          user = form.save()
          group = Group.objects.get(name='Members')
          user.groups.add(group)
          return redirect('login')
        else:
            return redirect('create_user')

    context = {
        "form":form,
    }
    return render(request, 'create_user.html', context )

@unauthenticated_user
def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)     
            return redirect('welcome_page')
        else:
            messages.info(request, 'username or password is not correct')  

    return render(request, 'login.html')

@login_required(login_url='login')
def welcome_page(request):
    user_profile = Profile.objects.filter(user=request.user).first()
    user_support_group = SupportGroup.objects.filter(profile = user_profile).first()
    if user_support_group:
        return redirect('group_dashboard')
    else:
        return render(request, 'welcome.html')
       

def Logout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def create_support_group(request):
    my_profile = Profile.objects.get(user = request.user)
    user_support_group = SupportGroup.objects.filter(profile = my_profile).first()
    if user_support_group:
        return redirect('group_dashboard')
    else:
        form = SupportGroupForm(initial={
            'profile':my_profile
        })
        if request.method == 'POST':
            form = SupportGroupForm(request.POST,request.FILES)
            if form.is_valid():
                # SupportGroup.profile = request.user
                # form.save(commit=False)
                form.save()
                # SupportGroup.save
                return redirect('group_dashboard')

        context = {
            'form':form
        }

    return render(request, 'create_support_group.html', context)

@login_required(login_url='login')
def support_group_detail(request,pk):
    support_group = SupportGroup.objects.get(id = pk)
    context = {
        'support_group':support_group
    }
    context = {
        'support_group':support_group,
    }
    return render(request, 'support_group_detail.html', context)

@login_required(login_url='login')
def update_support_group(request, pk):
    support_group = SupportGroup.objects.get(id = pk)
    form = SupportGroupForm(instance=support_group)
    if request.method == 'POST':
        form = SupportGroupForm(request.POST,request.FILES,instance=support_group)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')

    context = {
        'form':form
    }
    return render(request, 'update_support_group.html', context)


@login_required(login_url='login')
def delete_support_group(request, pk):
    support_group = SupportGroup.objects.get(id = pk)
    if request.method == 'POST':
        support_group.delete()
        return redirect('admin_dashboard')

    context = {
        'support_group':support_group
    }
    return render(request, 'delete_support_group.html', context)


def team(request):
    our_team = Team.objects.all()
    
    context = {
        'our_team':our_team
    }
    return render(request, 'our_team.html', context)


@login_required(login_url='login')
@admin_only_url
def admin_dashboard(request):
    my_user = Profile.objects.get(user = request.user)
    group = SupportGroup.objects.get(profile=my_user)
    support_groups = SupportGroup.objects.all()
    total = support_groups.count()
    context = {
        'support_groups':support_groups,
        'total':total,
        'group':group,
    }
    return render(request, 'dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Members', 'Teams'])
def group_dashboard(request):
    my_user = Profile.objects.get(user = request.user)
    group = SupportGroup.objects.get(profile=my_user)
    context = {
        'group':group,
    }
    return render(request, 'group_dashboard.html', context)