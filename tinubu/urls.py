from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('our_team', views.team, name='our_team'),
    path('create_user', views.create_user, name='create_user'),
    path('login', views.Login, name='login'),
    path('welcome_page', views.welcome_page, name='welcome_page'),
    path('logout', views.Logout, name='logout'),
    path('admin_dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('group_dashboard', views.group_dashboard, name='group_dashboard'),
    path('create_support_group', views.create_support_group, name='create_support_group'),
    path('support_group_detail/<str:pk>', views.support_group_detail, name='support_group_detail'),
    path('update_support_group/<str:pk>', views.update_support_group, name='update_support_group'),
    path('delete_support_group/<str:pk>', views.delete_support_group, name='delete_support_group'),
]

