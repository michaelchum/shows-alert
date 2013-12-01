from bs4 import BeautifulSoup
import re
import urllib2
""" 
redditFile = urllib2.urlopen("http://www.reddit.com")
redditHtml = redditFile.read()
redditFile.close()
 
soup = BeautifulSoup(redditHtml)
redditAll = soup.find_all("a")
for links in soup.find_all('a'):
    print (links.get('href')) """

def getListOfTopShows():

	listOfTopShows = []

	watchseriesusFile = urllib2.urlopen("http://watchseriesus.com/popular/")
	watchseriesusHtml = watchseriesusFile.read()
	watchseriesusFile.close()

	soup = BeautifulSoup(watchseriesusHtml)

	#for row in soup.find_all('td'):
	# for row in soup.find_all('ul', {'class' : 'lcp_catlist'}):
	# 	for title in row.find_all('li'):
	# 		print(title.a.get('title'))

	row = soup.find_all('ul', {'class' : 'lcp_catlist'})
	for title in row[0].find_all('li'):
		#print(title.a.get('title'))
		listOfTopShows.append(title.a.get('title'))

	return listOfTopShows

result = getListOfTopShows()

for i in result:
	print(i)