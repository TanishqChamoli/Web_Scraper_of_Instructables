from bs4 import BeautifulSoup
import requests
import json

if __name__ == "__main__":
	lst = []
	urls = ['https://www.instructables.com/Building-a-Self-Driving-Boat-ArduPilot-Rover/',
	'https://www.instructables.com/Hydraulic-Craft-Stick-Box/',
	'https://www.instructables.com/How-to-Make-a-Self-Watering-Plant-Stand/']
	for link in urls:
		source = requests.get(link).text
		soup = BeautifulSoup(source,'lxml')
		
		#getting the link of the first image which is being dynamically loaded
		#using json conversion of the data and then getting the data from the scrip tage and inserting it
		data = json.loads(soup.find("script",type='application/ld+json').string)
		image_url = data["image"]['url']

		# getting the header title
		header= soup.find('header',class_='article-header')
		header_title = header.h1.text
		
		# the given link
		scraped_url = link;

		# initialising the variables
		view_count = ''
		favourite_count = ''
		comment_count =''

		# for the main header part to get views , fav and comment this vcf
		vcf = header.div.findChildren() 
		
		# this is for the views
		view_count = vcf[5].text
		
		# this is for the fav part
		favourite_count = vcf[6].text
		
		# this is for the comment part
		if str(vcf[7].text) != "Featured":
			comment_count = vcf[7].text
		
#		this is for the youtube url
		main = soup.find('div',class_ = 'main-content')

		try:
			youtube_url = main.find('iframe')['src']
		except:
			youtube_url = ''
		
		# steps_titles
		step_titles = []
		all_steps = main.find_all('h2',class_="step-title")
		for steps in all_steps[1:]:
			step_titles.append(steps.text)

		# supplies
		supplies=[]
		try:
			# this is for the first kind of template in which they are stored in a li - list element
			ls = main.find('div',class_='step-body')
			if(ls.h3.text!=None):
				sup = ls.find_all('li')
				for x in sup:
					supplies.append(x.text)
		except:
			pass
		try:
			# this is for the second kind of templates to be handled in which they are stored in a p tag
			ls = main.find('div',class_='step-body')
			if(ls.h3.text!=None):
				sup = ls.find_all('p')
				for s in sup[2:]:
					# removing the extra data which was causing issues in this part
					supplies.append(s.text.replace("\u00b7       ",""))
		except:
			supplies.append("Not found")

		dic = {'header_title':header_title,'scraped_url':scraped_url,
		'youtube_url':youtube_url,'image_url':image_url,
		'view_count':view_count,'favourite_count':favourite_count,
		'comment_count':comment_count,'step_titles':step_titles,'supplies':supplies}
		lst.append(dic)
	print(json.dumps(lst))
