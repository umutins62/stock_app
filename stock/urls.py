"""
URL configuration for djangoStockApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("track_list/", views.track_list, name="track_list"),
    path("stock_list/", views.stock_list, name="stock_list"),
    path("principal/", views.principal, name="principal"),
    path("account/", views.account, name="account"),
    path("add_stock/", views.add_stock, name="add_stock"),
    path("delete_item/<int:id>", views.delete_item, name="delete_item"),
    path('update/<int:id>/', views.update_item, name='update_item'),
    path("change_pass/", views.change_password, name="change_pass"),
    path('add_track/', views.add_transaction, name='add_track'),
    path('add_money/', views.add_money, name='add_money'),
    path('update_money/', views.update_money, name='update_money'),
    path('update_track/<int:id>/', views.update_track, name='update_track'),

]
