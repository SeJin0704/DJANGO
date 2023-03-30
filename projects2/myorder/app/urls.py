from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('add/',views.add),
    path('search/',views.search),
    path('read/<int:id>/',views.read),
    path('read/<int:id>/delete/',views.delete),
    path('read/<int:id>/update/',views.update)
]