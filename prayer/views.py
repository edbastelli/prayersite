from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("\"Rejoice always, pray without ceasing, give thanks in all circumstances; for this is the will of God in Christ Jesus for you.\"<br> - 1 Thessalonians 5:16-18 (ESV)")
