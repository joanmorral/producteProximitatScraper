import requests
from bs4 import BeautifulSoup
import argparse
from datetime import datetime
import pandas as pd
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


def producte(llista_subsubcategories):
    nova_fila = {}
    df = pd.DataFrame()
    for llista_subsubcategories_url in llista_subsubcategories:
        print(llista_subsubcategories_url.split(';')[0])
        page4 = requests.get(llista_subsubcategories_url.split(';')[1])
        soup4 = BeautifulSoup(page4.content, 'html.parser')

        for categoria4 in soup4.find_all('div', class_='base__Body-sc-7vdzdx-29 bwaBvn'):
            enllac_producte = 'https://www.compraonline.bonpreuesclat.cat' + categoria4.a.get('href')
            print(enllac_producte)
            caracteristiques = info_prod_alimentacio(enllac_producte)
            print(caracteristiques)
            try:
                nova_fila = {'cadena': 'BonPreu',
                             'nom_producte': caracteristiques[0],
                             'format': caracteristiques[1],
                             'preu': caracteristiques[2].replace('\xa0', '').replace('€', '').replace('\xa0€', '').replace(
                                 ',', '.'),
                             'preu_volum': caracteristiques[3],
                             'info_prod': caracteristiques[4],
                             'marca': caracteristiques[5],
                             'descr_add': caracteristiques[6],
                             'ingredients': caracteristiques[7],
                             'dades_nutri': caracteristiques[8]
                            ,'instr': caracteristiques[9]
                              }
                #print(nova_fila)
                df = df.append(nova_fila, ignore_index=True)
            except:
                print('error' + nova_fila)
    return df

def guardaCSV(df):
    df.to_csv('BonPreu-Llistat_de_productes.csv', index=False)
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
