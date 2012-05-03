# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

def index(request):
    password = "hello"
    test = 1
    sensible = 2
    1/0
    return render_to_response('base/index.html', context_instance=RequestContext(request))
