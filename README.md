# productesProximitatScraper

## Resum

Sovint comprem productes sense conèixer la seva procedència. 
Amb la voluntat de fomentar el quilòmetre 0, el scraper captura els productes del catàleg de Bonpreu-Esclat en la recerca de l'origen dels productes.
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
- **productesProximitat_bonpreu.csv:**
- **Practica1_respostes.pdf:** 
- **Practica1_video.mp4:** 

## DOI del dataset generat

El dataset generat porta per títol ***Proximitat dels productes venuts a Bonpreu-Esclat***.  
Es troba emmagatzemat en format CSV a Zenodo, amb DOI: 

## Instruccions d'execució

### Càrrega de llibreries necessàries
Per executar el script és necessari instal·lar les següents biblioteques:

```python
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
from geopy.geocoders import Nominatim
from geopy import distance
```

### Descàrrega del llistat de productes
Per a descarregar la llista del supermercat BonPreu-Esclat cal emprar la següent instrucció:
```python
python productesProximitatScraper.py --baixallista bp
```
![img.png](img/captura_procescarregaproductes.png)

**Figura 1.** Captura del procés de càrrega

### Consulta de la distància dels articles d'una llista de la compra
La commanda per executar la consulta consta de dos paràmetres:
- paràmetre **--localitat** per posar el CP i població del consumidor
- paràmetre **--llista** acompanyat dels noms dels articles de la tenda de BonPreu-Esclat, cada nom s'ha de posar entre cometes i separant els articles amb espais: **"producte1" "producte2" "producte3"** ... 

A continuació es presenta un exemple: 
```python
python productesProximitatScraper.py --localitat 08202 Sabadell --llista "NOCILLA Crema de cacau amb avellanes" "EL PASTORET Iogurt estil grec artesà ecològic" "BIMBO Panets rodons per hamburgueses" "FERRER Cigrons cuits" "BONDUELLE Blat de moro ecològic" "FERRER Allioli" "YOSOY Beguda de civada ecològica" "COMPTA OVELLES Vi negre DO Penedès Km0" "SANT ANIOL Aigua mineral natural 6x1,5 L"
```

![img.png](img/captura_consultadistanciaproductes.png)
**Figura 2.** Captura del procés de consulta de distància de productes

![img_1.png](img/captura_mapadistanciaproductes.png)
**Figura 3.** Captura del mapa que es desplega amb el posicionament de productes


