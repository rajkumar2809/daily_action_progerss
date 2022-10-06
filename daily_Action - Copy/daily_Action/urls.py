"""daily_Action URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import imp
from django.contrib import admin
from django.urls import path
from daily_app import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index , name="index"),
    path('register/', views.register , name="register"),
    path('profile_register/', views.profile_reg , name="profile_reg"),
    path('login/', views.login , name="login"),
    path('loginUser/', views.loginUser , name="loginUser"),
    path('lead_dashboard/<id>', views.lead_dashboard , name="lead_dashboard"),
    path('create_group/<id>', views.create_group , name="create_group"),
    path('group_create/<id>', views.group_create , name="group_create"),
    
    path('dashboard/', views.dashboard , name="dashboard"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("view_employee/", views.view_employee, name="view_employee"),
    path("view_group/<id>", views.view_group, name="view_group"),

    path("view_member/", views.view_member, name="view_member"),
    # path("individual_group/<id>", views.individual_group, name="individual_group"),
    path("individual_group/<gid>", views.individual_group, name="individual_group"),
    path("member_dashboard/<id>", views.member_dashboard, name="member_dashboard"),
    path("admin_dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("add_members/<id>", views.add_members, name="add_members"),
    path("remove_member_from_group/", views.remove_member_from_group, name="remove_member_from_group"),
    path("view_groups_for_member/<id>", views.view_groups_for_member, name="view_groups_for_member"),
    path("create_project/<id>", views.create_project, name="create_project"),
    path("member_tasks/<id>", views.member_tasks, name="member_tasks"),
    path("update_task/", views.update_task, name="update_task"),
    path("update_task_after_submit/", views.update_task_after_submit, name="update_task_after_submit"),
    path("update_task_after_closed/", views.update_task_after_closed, name="update_task_after_closed"),
    path("view_tasks_as_per_group/", views.view_tasks_as_per_group, name="view_tasks_as_per_group"),
    path("add_notes/<id>", views.add_notes, name="add_notes"),
    path("to_do_update/<id>", views.to_do_update, name="to_do_update"),
    path("to_do_remove/<id>", views.to_do_remove, name="to_do_remove"),
    path("to_do_hold_for_now/<id>", views.to_do_hold_for_now, name="to_do_hold_for_now"),
    path("chat/<str:user_name>/", views.chat, name="chat"),
    path("/save_message/", views.save_message , name="save_message")
    


    
]
