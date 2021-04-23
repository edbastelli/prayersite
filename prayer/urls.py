from django.urls import path

from . import views

app_name = 'prayer'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('new/', views.newprayer, name='new prayer'),
    path('create/', views.createprayer, name='create prayer'),
    path('<int:prayer_id>/prayed/', views.prayed, name='prayed'),
]
