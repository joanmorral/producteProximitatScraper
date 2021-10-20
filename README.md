# producteProximitatScrapper

## Resum

Sovint comprem productes sense conèixer la seva procedència. 
Amb la voluntat de fomentar el quilòmetre 0, el scrapper captura els productes del catàleg de Bonpreu-Esclat en la recerca de l'origen dels productes.
Aleshores, amb l'ajuda d'una API trobem la longitud i latitud relatives al producte, de forma que en un futur permetin identificar la distància entre el productor i el consumidor.

El sistema permet respondre a preguntes com:
- Existeix un increment de cost entre el producte més pròxim i el més forani?
- Quins són els productes d'una llista de la compra més llunyans? Hi ha un producte alternatiu més pròxim al consumidor?
- Crear un conversor de productes de quilòmetre zero en funció de la ubicació del client.

## Context

Els elements d'aquest repositori constitueixen la resposta a la pràctica de web scraping de l'assignatura *Tipologia i Cicle de vida de les dades* del *Màster en Ciència de Dades* de la Universitat Oberta de Catalunya (UOC), corresponent al primer semestre del curs 2021-2022. Es tracta d'un treball realitzat amb fins acadèmics, i la totalitat dels resultats presentats es comparteixen a la comunitat perquè es pugin usar exclusivament amb fins no comercials.

## Grup de treball

El treball ha estat realitzat en grup, essent-ne els integrants:
- Joan Morral Ventura
- Nicolás González Soler

## Contingut del repositori

- **Readme.md:**
- **producteProximitatScrapper.py:**
- **Llistat_de_productes.csv:**  (canviar el nom ???)
- **Practica1_respostes.pdf:** 
- **Practica1_video.mp4:** 

## DOI del dataset generat

El dataset generat porta per títol ***Proximitat dels productes venuts a Bonpreu-Esclat***.  
Es troba emmagatzemat en format CSV a Zenodo, amb DOI: 

## Instruccions d'execució

Per executar el script és necessari instal·lar les següents biblioteques:

```python
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
from geopy.geocoders import Nominatim
from geopy import distance
```

El script s'ha d'executar de la següent manera:

```python
python producteProximitatScrapper.py --categories 'Llistes'
```

Per a poder identificar quines són les diferents categories de productes es pot consultar a través de la següent instrucció:


