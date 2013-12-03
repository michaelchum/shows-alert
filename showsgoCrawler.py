from bs4 import BeautifulSoup
import re
import urllib2
from episodes.models import TvShows
from sendEmail import send_email

""" 
redditFile = urllib2.urlopen("http://www.reddit.com")
redditHtml = redditFile.read()
redditFile.close()
 
soup = BeautifulSoup(redditHtml)
redditAll = soup.find_all("a")
for links in soup.find_all('a'):
    print (links.get('href')) """

def getLatestEpisodes(listOfShows):

	shows = listOfShows.keys()	

	showsgoHtmls = []
	showsgoFile = urllib2.urlopen("http://showsgo.com/")
	showsgoHtml = showsgoFile.read()
	showsgoHtmls.append(showsgoHtml)
	showsgoFile.close()

	for i in range(2, 11):
		text = "http://showsgo.com/page/%d"%i
		#print(text)
		showsgoFile = urllib2.urlopen(text)
		showsgoHtml = showsgoFile.read()
		showsgoHtmls.append(showsgoHtml)
		showsgoFile.close()	

	# soup = BeautifulSoup(showsgoHtml)

	# #print soup.ul.find_all('li')
	for show in shows:
		for page in showsgoHtmls:
			soup = BeautifulSoup(page)
			for links in soup.ul.find_all('li'):
				for url in links.find_all('div', {'class' : 'cover'}):
					#print(url.a.get('title') + " " + url.a.get('href'))
					if ( show.lower() in url.a.get('title').lower()):
						#print(url.a.get('href'))
						#listOfShows[show] = url.a.get('href')
						title = url.a.get('title')
						stream = url.a.get('href')
						listOfShows[show].append(stream)						
						#if title not in TvShows.objects.values_list('season_episode'):
						#print title
						p = TvShows(show_name=show , show_link=stream, season_episode=title)
						p.save()						
	return listOfShows


#testDict = {'Homeland' : [], 'Swamp Pawn' : [] , 'Monsters vs. Aliens': [], 'Jeopardy' : [], 'Time of Death' : [], 'The Mentalist': [], '2 Broke Girls': [], 'How I Met Your Mother' : [], 'The Blacklist': []} 
testDict = {'Mentalist': [], '2 Broke Girls': [], 'How I Met Your Mother' : [], 'The Blacklist': []} 

to = ['uehtesham90@gmail.com', 'usman.ehtesham@mail.mcgill.ca', 'michaelhochum@gmail.com']
#to = ['uehtesham90@gmail.com']
testDict = getLatestEpisodes(testDict)

# lastSeenId = ""
# rows = TvShows.objects.all() #.order_by('photo_id')
# for row in rows:
#   if row.season_episode == lastSeenId:
#     row.delete() # We've seen this id in a previous row
#   else: # New id found, save it and check future rows for duplicates.
#     lastSeenId = row.season_episode
# # for i in TvShows.objects.all():
# # 	if TvShows.objects.filter(show_link=i.show_link).count() > 1:
# # 		i.delete()

print len(TvShows.objects.all())

for key in testDict:
	s = 'Here is link to the latest episodes: \n'
	if len(testDict[key]) != 0 :
		for value in testDict[key]:
			s = s + value + '\n'
		send_email(to, key, s)