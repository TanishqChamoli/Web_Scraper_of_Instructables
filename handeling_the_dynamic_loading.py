from bs4 import BeautifulSoup
import requests
import json
if __name__ == "__main__":
	urls = ['https://www.instructables.com/Building-a-Self-Driving-Boat-ArduPilot-Rover/',
	'https://www.instructables.com/Hydraulic-Craft-Stick-Box/',
	'https://www.instructables.com/How-to-Make-a-Self-Watering-Plant-Stand/']
	for link in urls:
		source = requests.get(link).text
		soup = BeautifulSoup(source,'lxml')
		# we are using .string as in html parser and in lxml as well so we get this
		data = json.loads(soup.find("script",type='application/ld+json').string)
		print(data["image"]['url'])