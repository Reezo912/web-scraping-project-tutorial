from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import sqlite3

options = webdriver.ChromeOptions()

driver = webdriver.Chrome(
    service = Service(ChromeDriverManager().install()),
    options = options
)

# INDICO CUAL ES LA WEB QUE VOY A SCRAPEAR
driver.get('https://companies-market-cap-copy.vercel.app/index.html')


# ENCUENTRO LA PRIMERA TABLA Y LOS ENCABEZADOS DE LA MISMA
table = driver.find_element(By.CSS_SELECTOR, 'table')
headers = [header.text for header in table.find_elements(By.CSS_SELECTOR, 'th')]

# LISTA DONDE VAN A ESTAR LOS DATOS DE LA TABLA
data = []

# Divido la tabla en las filas que la componen
rows = table.find_elements(By.CSS_SELECTOR, 'tbody tr')

# Por cada una de las filas voy sacando los datos y los voy anadiendo a una lista para el df
for row in rows:
    casillas = row.find_elements(By.CSS_SELECTOR, 'td')
    data.append([casilla.text for casilla in casillas])

#print(data)

# Convierto en dataframe usando los headers
df = pd.DataFrame(data, columns=headers)

#print(df)

# QUITO LA COLUMNA QUE NO ME HACE FALTA Y LOS CARACTERES QUE NO QUIERO. CONVIERTO EN FLOAT Y QUITO LOS NA
df.drop('Change', axis=1, inplace=True)
df['Revenue'] = df['Revenue'].str.replace('$', '').str.replace('B', '').astype(float)
df.dropna(inplace=True)

# conecto la base de datos y creo el objeto cursor para interaccionar con ella
con = sqlite3.connect('tesla2.db')
cur = con.cursor()

# Ejecuto codigo SQL para crear la tabla con las columnas
cur.execute('''
CREATE TABLE IF NOT EXISTS revenue_table(
            year TEXT,
            revenue REAL
            )
''')

# INTRODUZCO LOS DATOS A LA TABLA DE SQL
df.to_sql('revenue_table', con, if_exists='replace', index=False)

# CONFIRMO CAMBIOS Y CIERRO LA CONEXION
con.commit()
print('Datos insertados correctamente')
con.close()