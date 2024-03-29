from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils import timezone
from django.urls import reverse
from django.views import generic
from django.contrib.auth.models import User
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
            return user.daily_list.get(date=date.today())
        except ObjectDoesNotExist:
            dlist = user.daily_list.create()
            daily_prayers=user.prayers.filter(frequency=1).exclude(expire_date__lt = date.today())
            rotating_prayers=user.prayers.filter(frequency=-1).exclude(expire_date__lt = date.today()).order_by('last_prayed_date')[:3]
            dlist.prayer.set(list(chain(daily_prayers, rotating_prayers)))
            dlist.save()
            return dlist

class MyPrayersView(generic.ListView):
    model = Prayer
    template_name = 'prayer/myprayers.html'

    def get_queryset(self):
        user=self.request.user
        return user.prayers.all().order_by('-created_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = date.today()
        return context

class DetailView(generic.DetailView):
    model = Prayer
    template_name = 'prayer/detail.html'

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
            )
            if request.POST['expire_date']:
                prayer.expire_date=request.POST['expire_date']
        except:
            return HttpResponse("Not sure what happened yet.")
        else:
            prayer.save()
            return HttpResponseRedirect(reverse('prayer:myprayers'))
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

class PrayerUpdateView(generic.edit.UpdateView):
    model = Prayer
    fields = ['prayer_title', 'prayer_text', 'expire_date', 'frequency']
    template_name_suffix = '_update_form'

    def get_queryset(self):
        user = self.request.user
        try:
            return user.prayers.filter(pk=self.kwargs['pk'])
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse('prayer:index'))

class PrayerFeed(generic.ListView):
    model = Prayer
    template_name = 'prayer/prayerfeed.html'

    def get_queryset(self):
        user=self.request.user
        return user.others_prayers.all().order_by('-created_date')

def addToMyList(request):
    if(request.method == 'POST'):
        prayer=Prayer.objects.get(pk=request.POST['prayer_id'])
        prayer.create_reference_prayer(request.user)
        return HttpResponseRedirect(reverse('prayer:myprayers'))
    else:
        return HttpResponseRedirect(reverse('prayer:index'))

def sharePrayer(request):
    if(request.method == 'POST'):
        prayer=Prayer.objects.get(pk=request.POST['prayerid'])
        sharewith=request.POST.getlist('userCheck')
        for userid in sharewith:
            prayer.visible_to.add(User.objects.get(pk=userid))
        prayer.save()
        return HttpResponseRedirect(reverse('prayer:myprayers'))
    else:
        return HttpResponseRedirect(reverse('prayer:myprayers'))

def email_daily_list(request):
    user=request.user
    try:
        dlist = user.daily_list.get(date=date.today())
    except ObjectDoesNotExist:
        dlist = user.daily_list.create()
        daily_prayers=user.prayers.filter(frequency=1).exclude(expire_date__lt = date.today())
        rotating_prayers=user.prayers.filter(frequency=-1).exclude(expire_date__lt = date.today()).order_by('last_prayed_date')[:3]
        dlist.prayer.set(list(chain(daily_prayers, rotating_prayers)))
        dlist.save()
