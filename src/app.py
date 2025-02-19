import os
from bs4 import BeautifulSoup
import requests
import time
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

url = "https://companies-market-cap-copy.vercel.app/index.html"

response = requests.get(url)
print(response)

if response.status_code != 200:
    print('No se ha encontrado la URL')

else:
    print('Se ha guardado la información')


html_response = BeautifulSoup(response.text, 'html.parser')

#print(html_response)

table = html_response.find("table")

print(table)

headers = [th.text for th in html_response.find("thead").find_all("th")]

data = []

for row in html_response.find("tbody").find_all("tr"):
    celdas = row.find_all("td")
    fila_datos = [celda.get_text(strip=True) for celda in celdas]
    data.append(fila_datos)

df = pd.DataFrame(data, columns=headers)
df = df.drop("Change", axis=1)
print(df)

df_limpio = df.dropna()

df_limpio['Revenue'] = df_limpio['Revenue'].str.replace('$', '').str.replace('B', '')

print(df_limpio)