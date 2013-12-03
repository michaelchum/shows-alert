from django.db import models

# Create your models here.
class Users(models.Model):
	name = models.CharField(max_length=100)
	email = models.CharField(max_length=100)
	password = models.CharField(max_length=8)

	def __unicode__(self):
		return self.name

class TvShows(models.Model):
	"""docstring foTvShowsme"""
	show_name = models.CharField(max_length=100)
	show_link = models.URLField(max_length=300)
	season_episode = models.CharField(max_length=300)
	name_list = models.ManyToManyField(Users)
	#name_list = ['uehtesham90@gmail.com', 'usman.ehtesham@mail.mcgill.ca']
	
	def __unicode__(self):
		return '%s %s %s' % (self.show_name, self.season_episode, self.show_link)

	def getShowName(self):
		return self.show_name

	def getShowLink(self):
		return self.show_link

	def getSeasonAndEpisode(self):
		return self.season_episode

	def getUsers(self):
		return self.name_list