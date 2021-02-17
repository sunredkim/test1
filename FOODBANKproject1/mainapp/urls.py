from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('test/', views.test, name='test'),
    path('logout/', views.logout, name='logout'),
    path('board/', views.board, name='board'),
    path('board/write/', views.board_write, name='write'),
    path('view/', views.view, name='view'),
    path('islike/', views.islike, name='islike'),
    path('notlike/', views.notlike, name='notlike'),
    path('update_cnt/', views.update_cnt, name='update_cnt'),
    path('mypage/', views.mypage, name='mypage'),
    path('userpost/', views.userpost, name='userpost'),
    path('remove/', views.remove, name='remove'),
    path('update/', views.update, name='update'),
    path('foodBankMap/', views.foodBankMap, name='foodBankMap'),
    path('centerItem/', views.centerItem, name='centerItem'),
    path('idx/', views.idx, name='idx'),
]