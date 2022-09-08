from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.models import Group
from . models import Profile, SupportGroup


def unauthenticated_user(view_func):
    def wrapper_func(request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('group_dashboard')
        else:
            return view_func(request,*args,**kwargs)
    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request,*args,**kwargs):
            group = None
            if request.user.groups:
                group=request.user.groups.all()[0].name
                # group = Group.objects.filter(user=request.user)
                if group in allowed_roles:
                   return view_func(request,*args,**kwargs)
                if group not in allowed_roles:
                    return HttpResponse('you are not allowed to view this page')

        return wrapper_func
    return decorator



def admin_only_url(view_func):
    def wrapper_func(request, *args,**kwargs):
        group = None
        if request.user.groups:
            group = request.user.groups.all()[0].name
            if group == 'Members':
                return redirect('group_dashboard')
            if group == 'Teams':
                return view_func(request,*args,**kwargs)
    return wrapper_func


