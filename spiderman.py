# Author: Antwan Love
# Webcrawler for search engine

import requests
import re
from bs4 import BeautifulSoup

# function to print links
def printLinks(self):
	for link in self.find_all(href=re.compile("/url")):
		url = (link.get("href"))
		print url.strip("/url?q=")

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
	userInput = raw_input("Please enter what you wish to find: ")
	
	results = searchGoogle(userInput)


# execute main function
if __name__ == "__main__":
	main()
