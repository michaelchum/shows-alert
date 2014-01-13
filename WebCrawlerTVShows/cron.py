#from django.core.management import setup_environ
#import settings

#setup_environ(settings)

# For reference: https://github.com/kraiz/django-crontab
from episodes.models import TvShows

def myJob():
	print TvShows.objects.all()

