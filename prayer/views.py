from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse
from .models import Prayer

# Create your views here.
def index(request):
    latest_prayer_list = Prayer.objects.order_by('last_prayed_date')[:20]
    context = {'latest_prayer_list': latest_prayer_list}
    return render(request, 'prayer/index.html', context)

def detail(request, prayer_id):
    prayer = get_object_or_404(Prayer, pk=prayer_id)
    return render(request, 'prayer/detail.html', {'prayer': prayer})

def newprayer(request):
    return render(request, 'prayer/newprayer.html')

def createprayer(request):
    try:
        prayer=Prayer(
            prayer_title=request.POST['prayertitle'],
            prayer_text=request.POST['prayertext'],
            created_date=timezone.now(),
            last_prayed_date=timezone.now(),
            frequency=1
        )
    except:
        return HttpResponse("Not sure what happened yet.")
    else:
        prayer.save()
        return HttpResponseRedirect(reverse('prayer:index'))
