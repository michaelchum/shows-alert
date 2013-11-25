# Create your views here.

from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

from episodes.models import TvShows

def index(request):
	# Request the context of the request
	# The context contains information such as the client's machine details for example.
	context = RequestContext(request)

def select_shows_list(request):
	# Request our context from the request passed to us.
	context = RequestContext(request)
	shows_list = TvShows.objects.all()
	context_dict = {'shows_list': shows_list}

	return render_to_response('episodes/select_shows_list.html', context_dict, context)

def about(request):
	# Request the context of the request
	# The context contains information such as the client's machine details for example.
	context = RequestContext(request)

def select_shows_search(request):
	# Request the context of the request
	# The context contains information such as the client's machine details for example.
	context = RequestContext(request)

def register(request):
	# Request the context of the request
	# The context contains information such as the client's machine details for example.
	context = RequestContext(request)