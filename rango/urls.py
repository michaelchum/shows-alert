from django.conf.urls import patterns, url
from rango import views

urlpatterns = patterns('', 
		url(r'^$', views.index, name='index'),
		url(r'^about/',views.about, name='about'),
		#url(r'^category/(?P<category_name_url>\w+)/$', views.category, name='category'),
		#url(r'^category/(?P<category_name_url>\w+)/add_page/$', views.add_page, name='add_page'),
		url(r'^show/(?P<show_name_url>\w+)/$', views.show, name='show'),
		url(r'^shows_list/', views.shows_list, name='shows_list'),
		url(r'^my_list/', views.my_list, name='my_list'),
		url(r'^register/$', views.register, name='register'),
		url(r'^login/$', views.user_login, name='login'),
		url(r'^logout/$', views.user_logout, name='logout'),
		url(r'^like_category/$', views.like_category, name='like_category'),
		url(r'^suggest_category/$', views.suggest_category, name='suggest_category'),
)

