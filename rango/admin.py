from django.contrib import admin
#from episodes.models import TvShows, UserProfile
from rango.models import TvShows, UserProfile
admin.site.register(TvShows)
admin.site.register(UserProfile)
#admin.site.register(User)
