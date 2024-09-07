from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import queue

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

def montagueDays(queue):
	service = Service(ChromeDriverManager().install())
	driver = webdriver.Chrome(service=service)

	url = f'https://howmanydayssincemontaguestreetbridgehasbeenhit.com'

	# Open the URL in the browser
	driver.get(url)

	try:
		# Wait for the page to load
		driver.implicitly_wait(5)

		# Find all elements with class
		elements = driver.find_element_by_class_name('jss25')

		if elements:
			days = elements.text
			print(days)
			queue.put(days)
		else:
			return("`Error: Number not found`")
	except Exception as e:
		return(f'Error: {e}')
	finally:
		driver.quit()
