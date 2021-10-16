# This is a sample Python script.
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
from geopy.geocoders import Nominatim
from geopy import distance

url = 'https://www.compraonline.bonpreuesclat.cat/products?source=navigation'

def getPage(url):
    '''
    Funció per capturar el contingut de la pàgina web
    :return: soup: contingut de la pàgina web
    '''
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    return soup


