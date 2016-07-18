import time
import urllib
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

urlInput = "http://" + input("Please enter an url (without the http:// in front): ")

# Keeps track of real time although not really accurate
startTime = time.time()

req = Request(urlInput)
try:
    response = urlopen(req)
except HTTPError as e:
    print('The server couldn\'t fulfill the request.')
    print('Error code: ', e.code)
    exit()
except URLError as e:
    print('We failed to reach a server.')
    print('Reason: ', e.reason)
    exit()
else:
    print('We are now going to scrap the url at', urlInput, 'works!')
    print("Status:", response.status, response.reason)

baseUrl = urlInput

soup = BeautifulSoup(response.read())

for link in soup.find_all('a'): 

	if (link.get('href').startswith("http")): 

		print (link.get('href'))

		linkReq = Request(link.get('href'))
		try:
		    linkResponse = urlopen(linkReq)
		except (HTTPError, URLError) as e:
		    print('The server couldn\'t fulfill the request for link:', link.get('href'),
		    	"Status:", e.code, e.reason)
		    exit()
		else:
		    print('The url to', link.get('href'), 'currently works.')
		    print("Status:", linkResponse.status, linkResponse.reason)

	elif (link.get('href').startswith("javascript:")): 
		pass

	else : 
		linkFullUrl = (urljoin(baseUrl, link.get('href')))
		print (linkFullUrl)

		linkReq = Request(linkFullUrl)

		try:
		    linkResponse = urlopen(linkReq)
		except (HTTPError, URLError) as e:
		    print('The server couldn\'t fulfill the request for link:', linkFullUrl,
		    	"Status:", e.code, e.reason)
		    exit()
		else:
		    print('The url to', linkFullUrl, 'currently works.')
		    print("Status:", linkResponse.status, linkResponse.reason)


print("And now we are done!")
print("It took a total of %s real-time seconds" % (time.time() - startTime))



