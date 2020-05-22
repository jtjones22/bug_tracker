"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path

from account import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='homepage'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add_ticket/', views.add_ticket_view, name='addticket'),
    path('ticket/<str:item_id>', views.ticket_view, name='ticket_detail'),
    path('ticket/edit_ticket/<str:item_id>', views.edit_ticket_view, name='edit_ticket'),
    path('ticket/assign_ticket/<str:item_id>', views.assign_ticket_view, name='assign_ticket'),
    path('ticket/return_ticket/<str:item_id>', views.return_ticket_view, name='return_ticket'),
    path('ticket/finish_ticket/<str:item_id>', views.finished_ticket_view, name='finish_ticket'),
    path('ticket/invalid_ticket/<str:item_id>', views.invalid_ticket_view, name='invalid_ticket'),
    path('profile/<str:item_id>', views.user_view, name='user_profile'),
]
