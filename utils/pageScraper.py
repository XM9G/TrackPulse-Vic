import requests
from bs4 import BeautifulSoup
from datetime import datetime

def transportVicSearch(search, tram=False):
	if tram:
		url = f'https://vic.transportsg.me/tram/tracker/fleet?fleet={search}'
	else:
		url = f'https://vic.transportsg.me/metro/tracker/consist?consist={search}'

	try:
		res = requests.get(url).text

		soup = BeautifulSoup(res, features="lxml")

		elements = soup.find_all('div', class_="trip")

		if not elements:
			return ["Error: No trips found. Train may be invalid or not currently running."]

		trip_texts = [element.text for element in elements]

		return trip_texts
	except Exception as e:
		return [f'Error: {e}']

def TRAMtransportVicSearch(search, tram=True):
	return transportVicSearch(search, tram=tram)

def montagueDays(q):
	url = "https://raw.githubusercontent.com/TeeWallz/monty_balboa/main/public/chumps.json"

	try:
		chumps = requests.get(url).json()

		days = (datetime.now() - datetime.strptime(chumps[0]["date"], "%Y-%m-%d")).days

		q.put(str(days))
	except Exception as e:
		return [f'Error: {e}']
