from django.urls import path
from django.contrib.auth import views as auth_view
#현재 폴더에서 views를 가지고 오는데 그 이름이,,,
from . import views as common_views

app_name = 'common'

urlpatterns = [
    path('', common_views.index, name = 'index'),
    path('login/', auth_view.LoginView.as_view(template_name = 'common/login.html'),name = 'login'),
    path('logout/', auth_view.LogoutView.as_view(),name = 'logout'),

    #회원가입
    #path('signup/',common_views.signup)

    path('signup/', common_views.signup_custom, name = 'signup'),
    #회원삭제
    path('delete/', common_views.delete, name = 'delete'),
    #회원수정
    path('update/', common_views.update, name = 'update'),

    #회원조회
    path('userinfo/', common_views.userinfo, name = 'userinfo'),

    
]