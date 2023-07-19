import re
import requests
import pandas as pd
from bs4 import BeautifulSoup

url = 'https://datosmacro.expansion.com/pib/ecuador'

fecha_list= []
pib_eur_list= []
pib_dol_list= []
variacion_list= []

#OBTENGO LA PAGINA A ANALIZAR
html_doc = requests.get(url)

#PARSEAR LA PAGINA WEB
soup = BeautifulSoup(html_doc.text, 'html.parser')

tabla = soup.find('table', attrs={'class': 'table tabledat table-striped table-condensed table-hover'})

#OBTENGO LAS FILAS DE LA TABLA
filas = tabla.find_all('tr')

for fila in filas:
    celdas= fila.find_all('td')
    if len(celdas)>0:
        fecha= celdas[0].string
        pib_eur= re.sub(r'[^\d.]', '', str(celdas[1].string))
        pib_dol= re.sub(r'[^\d.]', '', str(celdas[2].string))
        variacion= celdas[3].string
        fecha_list.append(fecha)
        pib_eur_list.append(pib_eur)
        pib_dol_list.append(pib_dol)
        variacion_list.append(variacion)

# print(fecha_list)
# print(pib_eur_list)
# print(pib_dol_list)
# print(variacion_list)

df = pd.DataFrame({'Fecha':fecha_list, 'PIB (Euros)':pib_eur_list, 'PIB (Dolares)': pib_dol_list, 'Variacion': variacion_list})
df.to_csv('pib_ecu.csv', index=False, encoding='utf-8')

