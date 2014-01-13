from django.db import models
from django.contrib.auth.models import User

class TvShows(models.Model):
	show_name = models.CharField(max_length=100)
	url = models.URLField(max_length=300, blank=True)
	picture_link = models.URLField(max_length=300, blank=True)
	likes = models.IntegerField(default=5)
	added = models.IntegerField(default=5)
	# season_episode = models.CharField(max_length=300)
	users = ['uehtesham90@gmail.com']
	#name_list = models.ManyToManyField(User)
	#users = models.ManyToManyField(User, blank=True)
	
	def __unicode__(self):
		return '%s %s' % (self.show_name, self.picture_link)

	def getShowName(self):
		return self.show_name

	def getUsers(self):
		return self.users

class Episode(models.Model):
	show = models.ForeignKey('TvShows')
	show_link = models.URLField(max_length=300)
	season_episode = models.CharField(max_length=300)
	sent = models.BooleanField(default=False)
	creation_date = models.DateTimeField(auto_now_add = True, editable=False)

	def __unicode__(self):
		return '%s %s %s' % (self.season_episode, self.show_link, self.sent)

	def getShowLink(self):
		return self.show_link

	def getSeasonAndEpisode(self):
		return self.season_episode


class UserProfile(models.Model):
	user = models.OneToOneField(User)
	show_list = models.ManyToManyField('TvShows')
	#latest_link = models.URLField(max_length=300)

	#def getLatestLink(self):
	#	return self.latest_link

	def getShowList(self):
		return self.show_list

	def __unicode__(self):
		return self.user.username