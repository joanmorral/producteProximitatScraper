import requests
from bs4 import BeautifulSoup
import argparse
from datetime import datetime
import pandas as pd
import re
from geopy.geocoders import Nominatim
from geopy import distance

url = 'https://www.compraonline.bonpreuesclat.cat/products?source=navigation'

#Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--categoria", help="Entra la categoria de productes")
args = parser.parse_args()

print(args)

def getPage(url):
    '''
    Funció per capturar el contingut de la pàgina web
    :param url:
    :return:
    '''
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup

def getCategories(soup):
    '''
    Funció per llegir les categories principals
    :param soup:
    :return:
    '''
    llista_categories=[]
    categories = soup.find('div', class_='spacing__Spacing-sc-5fzqe7-0 gegAoq')
    #print(categories.prettify())
    print('Llista de categories habilitades')
    print('=================================')
    for categoria in categories.find_all('a', class_='anchor__Anchor-sc-8ir86-0 ipYsWX'):
        llista_categories.append(categoria.text.strip() + ';' + 'https://www.compraonline.bonpreuesclat.cat' + categoria.get('href'))
        #print(categoria.text.strip() + ' - ' + 'https://www.compraonline.bonpreuesclat.cat' + categoria.get('href'))
        print(categoria.text.strip())
    return llista_categories

def getSubcategories(soup, llista_categories):
    '''

    :param soup:
    :param llista_categories:
    :return:
    '''
    llista_subcategories = []
    for llista_categories_url in llista_categories:
        print('============================')
        print(llista_categories_url.split(';')[0])
        print('============================')
        page2 = requests.get(llista_categories_url.split(';')[1])
        soup2 = BeautifulSoup(page2.content, 'html.parser')
        try:
            subcategories = soup2.find('div', class_='spacing__Spacing-sc-5fzqe7-0 gegAoq')
            for subcategoria in subcategories.find_all('a', class_='anchor__Anchor-sc-8ir86-0 ipYsWX'):
                llista_subcategories.append(
                    subcategoria.text.strip() + ';' + 'https://www.compraonline.bonpreuesclat.cat' + subcategoria.get(
                        'href'))
                #print(subcategoria.text.strip() + ' - ' + 'https://www.compraonline.bonpreuesclat.cat' + subcategoria.get(
                #    'href'))
                print(subcategoria.text.strip())
        except:
            # En cas que no hi hagi subcategoria ha de romandre l'anterior com a terminal
            #llista_subcategories.append(subcategories)
            #print(llista_categories_url.split(';')[0] + ',' + llista_categories_url.split(';')[1])
            llista_subcategories.append(
                    subcategoria.text.strip() + ';' + llista_categories_url.split(';')[1])
    return llista_subcategories


def info_prod_alimentacio(enllac_producte):
    '''
    Busca les característiques del producte i els retorna amb una llista
    RETURN: List nom_producte[0] - format[1] - preu[2] - preu_litre[3] - info_prod[4] - marca[5] - descr_add[6] - ingredients[7] - dades_nutri[8] - instr[9]
    '''
    caracteristiques = []
    pagina_producte = requests.get(enllac_producte)
    pagina_producte = BeautifulSoup(pagina_producte.content, 'html.parser')
    # nom producte
    caracteristiques.append(pagina_producte.find('div', class_='spacing__Spacing-sc-5fzqe7-0 gnwvlL').h1.text)
    # format
    caracteristiques.append(pagina_producte.find('span', class_='text__Text-x7sj8-0 bupnEA').text)
    # preu
    caracteristiques.append(pagina_producte.find('div', class_='spacing__Spacing-sc-5fzqe7-0 dsIaSZ').text)
    # preu litre
    caracteristiques.append('')

    info = pagina_producte.find('div', class_='Col-sc-3u3i8h-0 gRPIeN')
    for s in info.find_all('div', class_='static-content-wrapper__StaticContentWrapper-sc-1dfgbbt-0 Ziamt'):
        caracteristiques.append(s.text)
        #print(s.text)

    return caracteristiques

def nom_prod(caracteristiques):
    '''

    :param caracteristiques:
    :return:
    '''
    try:
        nom = caracteristiques[0]
    except:
        nom = 'NULL'
    return nom

def format_prod(caracteristiques):
    '''
    
    :param caracteristiques: 
    :return: 
    '''''
    try:
        #print(característiques[1])
        format = caracteristiques[1]
    except:
        format='NULL'
    return format

def preu_prod(caracteristiques):
    '''

    :param caracteristiques:
    :return:
    '''
    try:
        preu = caracteristiques[2].replace('\xa0', '').replace('€', '').replace('\xa0€', '').replace(',', '.')
    except:
        preu = 'NULL'
    return preu

def preu_vol_prod(caracteristiques):
    '''

    :param caracteristiques:
    :return:
    '''
    try:
        preu_vol = caracteristiques[3].replace('\xa0', '').replace('€', '').replace('\xa0€', '').replace(',', '.')
    except:
        preu_vol = 'NULL'
    return preu_vol

def info_prod(caracteristiques):
    '''

    :param caracteristiques:
    :return:
    '''
    try:
        info = caracteristiques[4]
    except:
        info = 'NULL'
    return info

def marca_prod(caracteristiques):
    '''

    :param caracteristiques:
    :return:
    '''
    try:
        marca = caracteristiques[5]
    except:
        marca = 'NULL'
    return marca

def direccio_prod(caracteristiques):
    '''

    :param caracteristiques:
    :return:
    '''
    try:
        #print(característiques[6])
        CP = re.findall('\d{5}', caracteristiques[6].split("Avís", 1)[0])[0]
        direccio = CP + ',' + caracteristiques[6].split("Avís", 1)[0].split(CP, 1)[1].replace('.', '')
    except:
        direccio='NULL'
    return direccio

def ingredients_prod(caracteristiques):
    '''

    :param caracteristiques:
    :return:
    '''
    try:
        ingredients = caracteristiques[7]
    except:
        ingredients = 'NULL'
    return ingredients

def nutri_prod(caracteristiques):
    '''

    :param caracteristiques:
    :return:
    '''
    try:
        nutri = caracteristiques[8]
    except:
        nutri = 'NULL'
    return nutri

def instr_prod(caracteristiques):
    '''

    :param caracteristiques:
    :return:
    '''
    try:
        instruccions = caracteristiques[9]
    except:
        instruccions = 'NULL'
    return instruccions

def localitzacio(direccio):
    '''

    :param direccio:
    :return:
    '''
    try:
        geolocator = Nominatim(user_agent="myapp")
        location = geolocator.geocode(direccio)
    except:
        location = 'NULL'
    return location

def latitud_prod(location):
    '''

    :param location:
    :return:
    '''
    try:
        latitud = location.latitude
    except:
        latitud = 0
    return latitud

def longitud_prod(location):
    '''

    :param location:
    :return:
    '''
    try:
        longitud = location.longitude
    except:
        longitud = 0
    return longitud

def retard_engany():
    '''

    :return:
    '''

    return

def producte(llista_subsubcategories):
    '''

    :param llista_subsubcategories:
    :return:
    '''
    nova_fila = {}
    df = pd.DataFrame()
    for llista_subsubcategories_url in llista_subsubcategories:
        print(llista_subsubcategories_url.split(';')[0])
        page4 = requests.get(llista_subsubcategories_url.split(';')[1])
        soup4 = BeautifulSoup(page4.content, 'html.parser')

        for categoria4 in soup4.find_all('div', class_='base__Body-sc-7vdzdx-29 bwaBvn'):
            enllac_producte = 'https://www.compraonline.bonpreuesclat.cat' + categoria4.a.get('href')
            #print(enllac_producte)
            caracteristiques = info_prod_alimentacio(enllac_producte)
            print(caracteristiques)
            try:
                location = localitzacio(direccio_prod(caracteristiques))
                nova_fila = {'cadena': 'BonPreu',
                             'subcategoria': llista_subsubcategories_url.split(';')[0],
                             'nom_producte': nom_prod(caracteristiques),
                             'format': format_prod(caracteristiques),
                             'preu': preu_prod(caracteristiques),
                             'preu_volum': preu_vol_prod(caracteristiques),
                             'info_prod': info_prod(caracteristiques),
                             'marca': marca_prod(caracteristiques),
                             'direccio': direccio_prod(caracteristiques),
                             'latitud': latitud_prod(location),
                             'longitud': longitud_prod(location),
                             'ingredients': ingredients_prod(caracteristiques),
                             'dades_nutri': nutri_prod(caracteristiques),
                             'instr': instr_prod(caracteristiques)
                              }
                #print(nova_fila)
                df = df.append(nova_fila, ignore_index=True)
            except:
                print('error' + nova_fila)
                guardaCSV(df)
    return df

def guardaCSV(df):

    df.to_csv('Llistat_de_productes.csv', index=False)
    return


soup=getPage(url)
llista_categories=getCategories(soup)

filtrada=[]
for grup in llista_categories:
    #if grup.split(';')[0] == 'Alimentació' or grup.split(';')[0]=='Begudes' or grup.split(';')[0]=='Frescos' or grup.split(';')[0]=='Congelats' or grup.split(';')[0]=='Làctics i ous' or grup.split(';')[0]=='Eco, sense gluten i lactosa, vegetarians i vegans':
    if grup.split(';')[0] == 'Alimentació':
        filtrada.append(grup)

print(filtrada)
llista_categories = filtrada

llista_subcategories=getSubcategories(soup, llista_categories)
llista_2subcategories=getSubcategories(soup, llista_subcategories)
df = producte(llista_2subcategories)
guardaCSV(df)
