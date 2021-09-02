#Import modulues
import requests
import argparse
import re

#Set command line inputs
parser = argparse.ArgumentParser(description='Generate string based HTML scraper for specific element on a webpage.')
req = parser.add_argument_group('Required arguments')
parser.add_argument("-u", "--url", help="URL to website you wish to scrape.", required=True)
parser.add_argument("-s", "--string", help="Text of the element you wish to scrape.", required=True)
req = parser.parse_args()

#Query the website
html = requests.get(req.url).text
split = html.split(req.string)
count = len(split)

#Function for creating the split string
def slicer(text, size=10):
	first = html.split(req.string)[0]
	prefix = first[len(first)-size:]
	second = html.split(req.string)[1]
	suffix = second[:size]
	try:
		val = html.split(prefix)[1].split(suffix)[0]
		if val == req.string:
			print(f"The string slices you need are:\nhtml.split(\"{prefix}\")[1].split(\"{suffix}\")[0]")
	except:
		slicer(text,size+5)

#Get text before requested string
def getPre(text,size=10):
	first = text.split(req.string)[0]
	prefix = first[len(first)-size:]
	return re.sub("\n","",prefix)

#Get text after requested string
def getSuff(text,size=10):
	second = html.split(req.string)[1]
	suffix = second[:size]
	return re.sub("\n","",suffix)

#Fail case
if count == 1:
	print("String not found!")

#Ideal case, there only exists one instance of the string in the web page
if count == 2:
	slicer(html)

#If there exist more than one instance, allow user to decide on the correct one
if count > 2 and count <= 10:
	print("What text surrounds the element you\'re extracting?")
	c = 0
	for s in split:
		print(f"{c}) {getPre(s)} {req.string} {getSuff(s)}")
		c+=1
	ans = -1
	try:
		ans = int(input())
	except:
		print("Invalid input!")
	slicer(split[ans])

#Failsafe for cases where there are an unreasonable amount of instances
if count > 10:
	print("String was too vague! More than 10 results!")
