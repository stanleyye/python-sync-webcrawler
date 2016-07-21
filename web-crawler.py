#!/usr/bin/env python

import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

linksVisited = {}

def crawl(aLink, originalBaseUrl):

    try:
        req = requests.get(aLink)
    except requests.exceptions.RequestException as e:
        print e
        exit()

    soup = BeautifulSoup(req.read())

    for link in soup.find_all('a'):
    	if (link.get('href').startswith("http")):
    		print (link.get('href'))

    		try:
                linkReq = requests.get(link.get('href'))
    		except requests.exceptions.RequestException as e:
    		    print("The server couldn't fulfill the request for link:", link.get('href'), "Status:", e)
            else:
                if (linksVisited[link.get('href')] or (not(aLink.startswith(originalBaseUrl)))):
                    pass
                else:
                    linksVisited[link.get('href')] = 1
                    print(link.get('href'), "Status:", linkReq.status_code)
                    crawl(link.get('href'), originalBaseUrl)

    	elif (link.get('href').startswith("javascript:")):
    		pass

    	else:
    		linkFullUrl = urlparse.urljoin(originalBaseUrl, link.get('href'))
            print(linkFullUrl)

    		try:
                linkReq = requests.get(linkFullUrl)
    		except requests.exceptions.RequestException as e:
    		    print("The server couldn't fulfill the request for link:", linkFullUrl, "Status:", e)
            else:
                if (linksVisited[linkFullUrl] or (not(linkFullUrl.startswith(originalBaseUrl)))):
                    pass
                else:
                    linksVisited[link.get('href')] = 1
                    print(link.get('href'), "Status:", linkReq.status_code)
                    crawl(linkFullUrl, originalBaseUrl)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a domain.")
    parser.add_argument("link")
    args = parser.parse_args()
    if (args.link.startswith("http://") or args.link.startswith("https://")):
        crawl(args.link, args.link)
    else:
        crawl("http://" + args.link, "http://" + args.link)
