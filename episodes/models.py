from django.db import models
from django.contrib.auth.models import User

class TvShows(models.Model):
	show_name = models.CharField(max_length=100)
	show_link = models.URLField(max_length=300)
	season_episode = models.CharField(max_length=300)
	#name_list = ['uehtesham90@gmail.com', 'usman.ehtesham@mail.mcgill.ca']
	#name_list = models.ManyToManyField(User)
	users = models.ManyToManyField(User, blank=True)
	
	def __unicode__(self):
		return '%s %s %s' % (self.show_name, self.season_episode, self.show_link)

	def getShowName(self):
		return self.show_name

	def getShowLink(self):
		return self.show_link

	def getSeasonAndEpisode(self):
		return self.season_episode

	def getUsers(self):
		return self.users

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