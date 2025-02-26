from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd


options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument('--disable-extensions')
options.add_argument('--no-sandbox')
options.add_argument('--disable-infobars')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-browser-side-navigation')
options.add_argument('--disable-gpu')

driver = webdriver.Chrome(
    service = Service(ChromeDriverManager().install()),
    options = options
)


driver.get('https://companies-market-cap-copy.vercel.app/earnings.html')

tabla = driver.find_element(By.CSS_SELECTOR, 'table')
headers = [header.text for header in tabla.find_elements(By.CSS_SELECTOR, 'thead th')]

rows = tabla.find_elements(By.CSS_SELECTOR, 'tbody tr')

tabla_earnings = []

for row in rows:
    celdas = row.find_elements(By.CSS_SELECTOR, 'td')
    tabla_earnings.append([celda.text for celda in celdas])

df = pd.DataFrame(tabla_earnings, columns=headers)

print(df)

driver.close()