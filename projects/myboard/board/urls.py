from django.urls import path
from . import views

app_name = 'board'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('<int:id>/', views.read, name = 'detail'),
    
    path('write/', views.write, name = 'write'),

    path('<int:id>/update/', views.update, name = 'update'),

    path('<int:id>/delete/', views.delete, name = 'delete'),

    path('<int:id>/write_reply/', views.write_reply, name= 'write_reply'),

    #댓글삭제주소
    path('<int:id>/delete_reply/<int:rid>/', views.delete_reply, name= 'delete_reply'),

    path('<int:id>/update_reply/', views.update_reply, name = 'update_reply'),

    #Ajax
    path('callAjax/', views.call_ajax),

    path('load_reply/', views.load_reply),
]
