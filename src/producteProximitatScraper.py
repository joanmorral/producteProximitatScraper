import requests
from bs4 import BeautifulSoup
import argparse
import time
import pandas as pd
import re
from random import randrange
from geopy.geocoders import Nominatim
from geopy import distance

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--baixallista", help="Si indica que vols descarregar la llista")
parser.add_argument("--categoria", help="Entra la categoria dels productes que vols descarregar. Si no s'especifica "
                                        "es baixen tots els camps.")
parser.add_argument("--localitat", help="Introdueix CP del client", nargs="*", type=str)
parser.add_argument("--llista", help="Introdueix una llista de la compra", nargs="*", type=str)
args = parser.parse_args()
#print(args)


def getPage(url):
    '''
    Funció per capturar el contingut de la pàgina web
    :param url:
    :return:
    '''
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    supermercat = soup.title.contents[0].split(" ", 1)[0]
    return soup


def getCategories(soup):
    '''
    Funció per llegir les categories principals
    :param soup:
    :return:
    '''
    llista_categories = []
    categories = soup.find('div', class_='spacing__Spacing-sc-5fzqe7-0 gegAoq')
    # print(categories.prettify())
    print('Llista de categories habilitades')
    print('=================================')
    for categoria in categories.find_all('a', class_='anchor__Anchor-sc-8ir86-0 ipYsWX'):
        llista_categories.append(
            categoria.text.strip() + ';' + 'https://www.compraonline.bonpreuesclat.cat' + categoria.get('href'))
        # print(categoria.text.strip() + ' - ' + 'https://www.compraonline.bonpreuesclat.cat' + categoria.get('href'))
        print(categoria.text.strip())
    return llista_categories


def getSubcategories(soup, llista_categories):
    '''
    Funció per a llegir les subcategories d'una pàgina, serveix per subsubcatgories
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
                # print(subcategoria.text.strip() + ' - ' + 'https://www.compraonline.bonpreuesclat.cat' + subcategoria.get(
                #    'href'))
                print(subcategoria.text.strip())
        except:
            # En cas que no hi hagi subcategoria ha de romandre l'anterior com a terminal
            # llista_subcategories.append(subcategories)
            # print(llista_categories_url.split(';')[0] + ',' + llista_categories_url.split(';')[1])
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
        # print(s.text)

    return caracteristiques


def nom_prod(caracteristiques):
    '''
    Funció d'extracció del nom de producte
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
    Funció del format amb el que es presenta el producte
    :param caracteristiques: 
    :return: 
    '''''
    try:
        # print(característiques[1])
        format = caracteristiques[1]
    except:
        format = 'NULL'
    return format


def preu_prod(caracteristiques):
    '''
    Funció tractament del preu del producte
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
    Funció tractament del volum del producte
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
    Funció de tractament de la informació del producte
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
    Funció per extreure la marca del producte
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
    Funció per extreure la direcció del producte
    :param caracteristiques:
    :return:
    '''
    try:
        # print(característiques[6])
        CP = re.findall('\d{5}', caracteristiques[6].split("Avís", 1)[0])[0]
        direccio = CP + ',' + caracteristiques[6].split("Avís", 1)[0].split(CP, 1)[1].replace('.', '')
    except:
        direccio = 'NULL'
    return direccio


def ingredients_prod(caracteristiques):
    '''
    Funció per extreure els ingredients del producte
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
    Funció per extreure els valors nutricionals dels productes alimentaris
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
    Funció per extreure les dades de emmagatzematge dels productes
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
    Funció per aconseguir les dades corresponents a una direcció associada
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
    Funció per aconseguir la latitud un cop se li passa el conjunt d'informació de geoposicionament de Nominatim
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
    Funció per aconseguir la longitud un cop se li passa el conjunt d'informació de geoposicionament de Nominatim
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
    Funció per processar a l'engany del mecanisme de detecció de bots (tot i que no s'ha identificat a BonPreu)
    :return:
    '''
    time.sleep(randrange(5))
    return


def producte(llista_subsubcategories):
    '''
    Funció que navega per cada pàgina de producte de les seccions carregades a la llista i en captura la info en un dataframe
    :param llista_subsubcategories:
    :return:
    '''
    nova_fila = {}
    df = pd.DataFrame()

    # Consulta la data i la hora
    named_tuple = time.localtime()
    time_string = time.strftime("%Y%m%d", named_tuple)

    for llista_subsubcategories_url in llista_subsubcategories:
        print(llista_subsubcategories_url.split(';')[0])
        page4 = requests.get(llista_subsubcategories_url.split(';')[1])
        soup4 = BeautifulSoup(page4.content, 'html.parser')

        for categoria4 in soup4.find_all('div', class_='base__Body-sc-7vdzdx-29 bwaBvn'):
            enllac_producte = 'https://www.compraonline.bonpreuesclat.cat' + categoria4.a.get('href')
            # print(enllac_producte)
            caracteristiques = info_prod_alimentacio(enllac_producte)
            #print(caracteristiques)

            try:
                location = localitzacio(direccio_prod(caracteristiques))
                nova_fila = {'data': time_string,
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
                print(nova_fila)
                df = df.append(nova_fila, ignore_index=True)
            except:
                print('error' + nova_fila)
                guardaCSV(df, supermercat)
    return df


def guardaCSV(df):
    '''
    Funció encarregada de guardar la informació en un CSV
    :param df:
    :return:
    '''
    # Consulta la data i la hora
    #named_tuple = time.localtime()
    #time_string = time.strftime("%Y%m%d", named_tuple)
    # Defineix el nom del fitxer

    #nom_csv = time_string + '_' + supermercat + '_productes.csv'
    nom_csv = 'proximitat_productes_bonpreu.csv'
    df.to_csv(nom_csv, index=False)
    return


def baixaLlista(url):
    '''
    Funció per a descarregar la llista de productes del supermercat online
    :return:
    '''
    soup = getPage(url)
    llista_categories = getCategories(soup)

    filtrada = []
    for grup in llista_categories:
        if grup.split(';')[0] == 'Alimentació' or grup.split(';')[0]=='Begudes' or grup.split(';')[0]=='Frescos' or grup.split(';')[0]=='Congelats' or grup.split(';')[0]=='Làctics i ous' or grup.split(';')[0]=='Eco, sense gluten i lactosa, vegetarians i vegans':
        #if grup.split(';')[0] == 'Alimentació':
            filtrada.append(grup)

    print(filtrada)
    llista_categories = filtrada

    llista_subcategories = getSubcategories(soup, llista_categories)
    llista_2subcategories = getSubcategories(soup, llista_subcategories)
    df = producte(llista_2subcategories)
    guardaCSV(df)
    return


def consultaLlista(args):
    '''
    Funció encarregada de llegir la localització del client i calcular la distància fins a l'emrpresa productora
    :param args:
    :return:
    '''
    # Identificació del client
    posicio_client = localitzacio(args.localitat)
    # print(posicio_client)
    lat_client = latitud_prod(posicio_client)
    long_client = longitud_prod(posicio_client)
    geopos = (lat_client, long_client)
    print(geopos)

    # Carga CSV de consulta
    df = pd.read_csv('../csv/Llistat_de_productes.csv')

    # Cerca de proximitat en la llista
    for x in range(len(args.llista)):
        article = (args.llista[x])
        fabrica_loc = ((df[df['nom_producte'] == str(article)]['latitud'].iloc[0]),
                       (df[df['nom_producte'] == str(article)]['longitud'].iloc[0]))
        km = distance.distance(geopos, fabrica_loc).km
        print(article + '- proximitat:' + '%.2f' % km + 'km')
    return posicio_client


if args.baixallista == 'bp':
    # Enllaç a la tenda online de BonPreu
    url = 'https://www.compraonline.bonpreuesclat.cat/products?source=navigation'
    baixaLlista(url)

# python producteProximitatScraper.py --localitat 08202 Sabadell --llista "NOCILLA Crema de cacau amb avellanes" "GULLÓN Galetes de xocolata sense sucres" "BIMBO Panets rodons per hamburgueses" "FERRER Cigrons cuits" "BONDUELLE Blat de moro ecològic"
# consultaLlista(args)

