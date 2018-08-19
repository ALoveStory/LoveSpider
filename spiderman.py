# Author: Antwan Love (ADLJR)
# Webcrawler for search engine

import csv
import re
import requests
import sys
from bs4 import BeautifulSoup

# writing output to csv format
def outputCSV(self):
	outputFile = open('output.csv', 'w')
	with outputFile:
		writer = csv.writer(outputFile)
		writer.writerows([self])
	print "Output to CSV complete. Search has ended."


# function to print links
def printLinks(self):
	i = 1	
	newList = []
	for link in self.find_all(href=re.compile("/url")):
		htmlUrl = (link.get("href"))
		url = htmlUrl.strip("/url?q=")
		urlLine = '{0} {1}'.format(i, url)
		newList.append(urlLine)
		i += 1
	outputCSV(newList)
		

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
