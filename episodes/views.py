# Create your views here.

from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

def index(request):
	# Request the context of the request
	# The context contains information such as the client's machine details for example.
	context = RequestContext(request)