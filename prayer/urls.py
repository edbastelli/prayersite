from django.urls import path
from django.contrib.auth.decorators import login_required, user_passes_test

from . import views

app_name = 'prayer'
urlpatterns = [
    path('', login_required(views.IndexView.as_view()), name='index'),
    path('<int:pk>/', login_required(views.detail), name='detail'),
    path('new/', views.newprayer, name='new prayer'),
    path('create/', views.createprayer, name='create prayer'),
    path('<int:prayer_id>/prayed/', views.prayed, name='prayed'),
]
