from django.urls import path

from . import views

app_name = 'prayer'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:prayer_id>/', views.detail, name='detail'),
    path('new/', views.newprayer, name='new prayer'),
    path('create/', views.createprayer, name='create prayer'),
    path('<int:prayer_id>/prayed', views.prayed, name='prayed'),
]
