import json
from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
#ReturnJSON: return HttpResponse(json.dumps(valores), content_type="application/json")

def profile(request, summoner = None, idSum = None, region = None, info = None):
    context = RequestContext(request)
    return render_to_response('profile.html', context)


def chat(request, region = None, friend = None):
    print("#-----chat-----#")

def static(request, section = None, specific = None):
    print("#-----static-----#")

def home(request, section = None, specific = None):
    print("#-----static-----#")
