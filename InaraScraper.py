#Alex is the dankest of McGroreys
from lxml import html
import requests
import sys

class Element():
	def __init__(self, station, system, price):
		self.station = station
		self.system = system
		price = price.replace(',', '')
		self.price = int(price)

	def pprint(self):
		print(str(self.price)+"	at "+self.station+" in "+self.system)

def processSearch(item):
	try:
		itemCode = items[item]
		destURL = "https://inara.cz/goods/"+itemCode+"/#commodityslotsell"
		page = requests.get(destURL)
		tree = html.fromstring(page.content)
		#Get lists of info, will be indexed the same
		stations = tree.xpath('//span[@class="normal avoidwrap"]/text()')
		systems = tree.xpath('//span[@class="uppercase avoidwrap"]/text()')
		sellprice = tree.xpath('//td[@class="alignright"]/text()')
		#Strip out quantity values
		sellprice = sellprice[1::2]

		#sort and store
		elementList = []
		for x, y, z in zip(stations, systems, sellprice):
			elementList.append(Element(x, y, z))
		elementList.sort(key=lambda i: i.price, reverse=True)
		
		#Print list
		count = 0
		for elem in elementList:
			count=count+1
			if count < 51:
				elem.pprint()
			else:
				break
	except KeyError:
		print("Error processing search, "+item+" is not a recognized parameter, you dumb bitch.")
	

items = {"Void Opal": "10250", "Alexandrite": "10249", "Grandidierite": "10248", "Narcotics":"12", "Low Temperature Diamonds":"144", "Benitoite":"10247", "Painite":"84", "Serendibite":"10244", "Musgravite":"10246", "Monazite":"10245"}

if len(sys.argv) < 2:
	print("WELCOME TO INARA SCRAPER \nThis tool will return the top 50 sell locations for supported commodities. \nEnter -items for a list of the supported commodities.\n")
	print("Type \"q\" to exit gracefully.")

	inputMsg = "RESET"
	while inputMsg == "RESET":
		item = input("Search: ")
		#Check for options before processing search
		if item == "-items":
			print("\nSupported items: ")
			for key, value in items.items():
				print("-"+key)
		elif item == "quit":
			sys.exit()
		else:
			processSearch(item)
else:
	item = sys.argv[1]
	processSearch(item)

