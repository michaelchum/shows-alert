from django.db import models
from django.contrib.auth.models import User

class TvShows(models.Model):
	show_name = models.CharField(max_length=100)
	url = models.URLField(max_length=300)
	# season_episode = models.CharField(max_length=300)
	#name_list = ['uehtesham90@gmail.com', 'usman.ehtesham@mail.mcgill.ca']
	#name_list = models.ManyToManyField(User)
	users = models.ManyToManyField(User, blank=True)
	
	def __unicode__(self):
		return '%s ' % (self.show_name)

	def getShowName(self):
		return self.show_name

	def getUsers(self):
		return self.users

class Episode(models.Model):
	episode = models.ForeignKey('TvShows')
	show_link = models.URLField(max_length=300)
	season_episode = models.CharField(max_length=300)

	def __unicode__(self):
		return '%s %s' % (self.season_episode, self.show_link)

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