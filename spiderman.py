# Author: Antwan Love
# Webcrawler for search engine

import requests
from bs4 import BeautifulSoup

# function to print links
def printLinks(self):
	for link in self.find_all('a'):
		print(link.get('href')

# function to create a list of links
def createLinkList(self):
	extractLinks = BeautifulSoup(self.text, "html.parser")
	printLinks(extractLinks)

# function which forwards user input into the google search engine
def searchGoogle(self):
	searchsite = requests.get(
	"https://www.google.com/search",
	params = dict(
		query=self
	)) 
	
	createLinkList(searchsite)

# main
def main():
	userInput = raw_input("Please enter what you wish to find: ")
	
	results = searchGoogle(userInput)


# execute main function
if __name__ == "__main__":
	main()
