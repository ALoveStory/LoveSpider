# Author: Antwan Love
# Webcrawler for search engine

import re
import requests
import sys
from bs4 import BeautifulSoup

# function to print links
def printLinks(self):
	i = 1	
	for link in self.find_all(href=re.compile("/url")):
		url = (link.get("href"))
		print "(", i,")", url.strip("/url?q=")
		i+= 1

# function to create a list of links
def createLinkList(self):
	extractLinks = BeautifulSoup(self.text, "html.parser")
	printLinks(extractLinks)

# function which forwards user input into the google search engine
def searchGoogle(userInput):
	searchsite = requests.get(
		"https://www.google.com/search",
		params = dict(
			query=userInput
	)) 
	# call to function to create a list of links
	createLinkList(searchsite)

# main
def main():
	userInput = sys.argv[1:]
	
	results = searchGoogle(userInput)


# execute main function
if __name__ == "__main__":
	main()
