from bs4 import BeautifulSoup
import re
import urllib2
from episodes.models import TvShows
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
						listOfShows[show].append(url.a.get('href'))
						stream = url.a.get('href')
						p = TvShows(show_name=show , show_link=stream)
						p.save()						


	return listOfShows


testDict = {'Homeland' : [], 'Swamp Pawn' : [] , 'Monsters vs. Aliens': [], 'Jeopardy' : [], 'Time of Death' : [], 'The Mentalist': []} 

testDict = getLatestEpisodes(testDict)

for key in testDict:
	for value in testDict[key]:
		print key, value