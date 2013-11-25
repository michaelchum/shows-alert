from django.conf.urls import patterns, url
from episodes import views

urlpatterns = patterns('', 
		#url(r'^$', views.index, name='index'),
		#url(r'^about/',views.about, name='about'),
		url(r'^select_shows_list/$', views.select_shows_list, name='select_shows_list'),
		#url(r'^register/$', views.add_category, name='register'),
		#url(r'^category/(?P<category_name_url>\w+)/$', views.category, name='category'),
		#url(r'^category/(?P<category_name_url>\w+)/add_page/$', views.add_page, name='add_page'),
		)