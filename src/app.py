import os
from bs4 import BeautifulSoup
import requests
import time
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Guardo URL en una variable
url = "https://companies-market-cap-copy.vercel.app/index.html"

# Invoco la variable URL para obtener los datos de la misma 
response = requests.get(url)

# Codigo 200 indica que ha se ha obtenido respuesta
# Verificacion de que se ha obtenido respuesta
if response.status_code != 200:
    print('No se ha encontrado la URL')
else:
    print('Se ha guardado la información')

# Parseo de response en html para que sea mas facil de consultar
parsed_response = BeautifulSoup(response.text, 'html.parser')
#print(parsed_response)

# Encuentra la primera tabla e imprime la informacion
table = parsed_response.find(class_="table")
#print(table)

# Encuentra los headers(encabezados) de la tabla
# Como solo hay una tabla, se puede usar esta comprehensive list, sino habria que buscar la tabla que queremos
# Thead = engloba los encabezados de la tabla /// Th = Indica cada encabezado de la tabla
headers = [th.text for th in parsed_response.find("thead").find_all("th")]
#print(headers)

# Creamos la lista con los datos
data = []


# Buscamos los datos dentro del cuerpo de la tabla por cada una de las filas
for row in parsed_response.find("tbody").find_all("tr"):
    # Datos de todas las celdas de la fila
    celdas = row.find_all("td")
    # Se extraen los datos de cada una de las celdas de la fila // Strip quita los espacios antes y despues para extraer solo el texto
    fila_datos = [celda.get_text(strip=True) for celda in celdas]
    # Se añaden estos datos a la lista data
    data.append(fila_datos)


# Creamos el DataFrame en pandas a partir de la lista data, indicamos los nombres de las columnas
df = pd.DataFrame(data, columns=headers)


# Limpiamos los NA, quito los $ y las B y transformo a float
df_limpio = df.dropna()
df_limpio['Revenue'] = df_limpio['Revenue'].str.replace('$', '').str.replace('B', '').astype(float)
# Quito columna 'Change', no la voy a necesitar
df_limpio = df_limpio.drop("Change", axis=1)
# Añado unidades de medida borradas
df_limpio = df_limpio.rename(columns={'Revenue' : 'Revenue ($ per B)'})
print(df_limpio)
#print(df_limpio.dtypes)
#print(df_limpio)

# Hay que ordenar los valores segun la fecha

df_limpio = df_limpio.sort_values('Year')

# Conexion a base de datos SQLite3
con = sqlite3.connect('tesla.db')
cur = con.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS revenue_table(
            year TEXT,
            revenue REAL
            )
''')

df_limpio.to_sql('revenue_table', con, if_exists='replace', index=False)

con.commit()
print('Datos insertados correctamente')
con.close()


# Visualizacion de datos

# Grafico de lineas
plt.figure(figsize=(10, 6))
plt.plot(df_limpio["Year"], df_limpio["Revenue ($ per B)"], marker='o', label="Ingresos")
plt.title("Ingresos anuales de Tesla")
plt.xlabel("Fecha")
plt.ylabel("Ingresos en billones(USD)")
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)

# Guardar y mostrar el plot
plt.savefig("revenue_plot_lineas.png")
plt.show()


# Grafico de barras
plt.figure(figsize=(10,6))
plt.bar(df_limpio["Year"], df_limpio["Revenue ($ per B)"], color='skyblue', label="Ingresos")
plt.title("Ingresos anuales de Tesla")
plt.xlabel("Año")
plt.ylabel("Ingresos en billones (USD)")
plt.xticks(rotation=45)
plt.legend()
plt.grid(True, axis='y', linestyle='--', alpha=0.7)

# Guardar y mostrar el plot
plt.savefig("revenue_plot_Barras.png")
plt.show()

# Grafico de dispersion (Scatter plot)
plt.figure(figsize=(10,6))
plt.scatter(df_limpio["Year"], df_limpio["Revenue ($ per B)"], color='red', s=100, label="Ingresos")
plt.title("Ingresos anuales de Tesla")
plt.xlabel("Año")
plt.ylabel("Ingresos en billones (USD)")
plt.xticks(rotation=45)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)

plt.savefig("revenue_plot_Scatter.png")
plt.show()

