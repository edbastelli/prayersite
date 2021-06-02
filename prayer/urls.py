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
    path('<int:pk>/update/', login_required(views.PrayerUpdateView.as_view()), name='update_prayer'),
    path('myprayers', login_required(views.MyPrayersView.as_view()), name='myprayers'),
    path('prayerfeed', login_required(views.PrayerFeed.as_view()), name='prayerfeed'),
    path('addtomylist', login_required(views.addToMyList), name='addtomylist'),
]
