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
		#url(r'^like_category/$', views.like_category, name='like_category'),
		url(r'^add_show/$', views.add_show, name='add_show'),
		url(r'^remove_show/$', views.remove_show, name='remove_show'),
		url(r'^remove_show2/$', views.remove_show2, name='remove_show2'),
		url(r'^add_from_show/$', views.add_from_show, name='add_from_show'),
		url(r'^remove_from_show/$', views.remove_from_show, name='remove_from_show'),
		url(r'^suggest_category/$', views.suggest_category, name='suggest_category'),
		url(r'^profile/$', views.profile, name='profile'),
		url(r'^add_email/$', views.add_email, name='add_email'),
		url(r'^remove_email/$', views.remove_email, name='remove_email'),
		url(r'^add_sms/$', views.add_sms, name='add_sms'),
		url(r'^remove_sms/$', views.remove_sms, name='remove_sms'),
)

