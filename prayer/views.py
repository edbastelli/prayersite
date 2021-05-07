from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils import timezone
from django.urls import reverse
from django.views import generic
from .models import Prayer, DailyPrayerList
from itertools import chain
from datetime import date, datetime
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
class IndexView(generic.ListView):
    model = DailyPrayerList
    template_name = 'prayer/index.html'
    context_object_name = 'latest_prayer_list'

    def get_queryset(self):
        user=self.request.user
        try:
            # return user.daily_list.get(date=date.today()).prayer.all()
            return user.daily_list.get(date=date.today())
        except ObjectDoesNotExist:
            dlist = user.daily_list.create()
            daily_prayers=user.prayers.filter(frequency=1)
            rotating_prayers=user.prayers.filter(frequency=-1).order_by('last_prayed_date')[:3]
            dlist.prayer.set(list(chain(daily_prayers, rotating_prayers)))
            dlist.save()
            # return user.daily_list.get(date=date.today()).prayer.all()
            return dlist

class DetailView(generic.DetailView):
    model = Prayer
    template_name = 'prayer/detail.html'

# def index(request):
#     latest_prayer_list = Prayer.objects.order_by('last_prayed_date')[:20]
#     context = {'latest_prayer_list': latest_prayer_list}
#     return render(request, 'prayer/index.html', context)

def detail(request, pk):
    prayer = get_object_or_404(Prayer, pk=pk)
    if prayer.user == request.user:
        return render(request, 'prayer/detail.html', {'prayer': prayer})
    else:
        return HttpResponseRedirect(reverse('prayer:index'))

def newprayer(request):
    return render(request, 'prayer/newprayer.html')

def createprayer(request):
    if(request.method == 'POST'):
        try:
            prayer=Prayer(
                prayer_title=request.POST['prayertitle'],
                prayer_text=request.POST['prayertext'],
                created_date=timezone.now(),
                last_prayed_date=timezone.now(),
                user=request.user,
                frequency=request.POST['frequency'],
                expire_date=request.POST['expire_date']
            )
        except:
            return HttpResponse("Not sure what happened yet.")
        else:
            prayer.save()
            return HttpResponseRedirect(reverse('prayer:index'))
    else:
        return HttpResponseRedirect(reverse('prayer:index'))

def prayed(request, prayer_id):
    if(request.method  == 'POST'):
        try:
            prayer=Prayer.objects.get(pk=request.POST['prayer_id'])
            prayer.update_last_prayed()
        except:
            HttpResponse("Got an exception in prayed")
        else:
            prayer.save()
            return HttpResponseRedirect(reverse('prayer:index'))
    else:
        prayer = get_object_or_404(Prayer, pk=prayer_id)
        return HttpResponseRedirect(reverse('prayer:detail', args=(prayer_id,)))
