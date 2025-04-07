from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import time
from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
email = os.getenv("TWITTER_EMAIL")
username = os.getenv("TWITTER_USERNAME")
password = os.getenv("TWITTER_PASSWORD")

# --------- 1. Función para scrapear valores del dólar ---------
def get_dollar_prices():
    url = 'https://dolarhoy.com/'
    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'html.parser')

    buy_divs = soup.find_all('div', class_='compra')[1:6]
    sell_divs = soup.find_all('div', class_='venta-wrapper')[0:5]

    buy = []
    sell = []

    for div in buy_divs:
        val = div.find('div', class_='val')
        if val:
            value = val.text.split('$')[1].replace(',', '.')
            buy.append(value)

    for div in sell_divs:
        val = div.find('div', class_='val')
        if val:
            value = val.text.split('$')[1].replace(',', '.')
            sell.append(value)

    columns = ['Dolar Blue', 'Dolar Oficial', 'Dolar Mep', 'Contado con Liqui', 'Dolar Cripto']
    df = pd.DataFrame(data=[buy, sell], columns=columns, index=['Compra', 'Venta'])

    return df

# --------- 2. Función para generar texto del tweet ---------
def generate_tweet_text(df):
    tweet = f"Cotización del Dólar Hoy {datetime.today().strftime('%d/%m/%y')} - {datetime.today().strftime('%H:%M')} \n\n"
    for col in df.columns:
        tweet += f"{col}: Compra {df[col]['Compra']} - Venta {df[col]['Venta']}\n"
    return tweet

# --------- 3. Función para loguearse en X ---------
def login_to_x(driver, email, username, password):
    driver.get('https://x.com/')
    driver.maximize_window()
    action = ActionChains(driver)
    time.sleep(3)

    # Cookies
    try:
        driver.find_element(By.XPATH, '/html/body/div/div/div/div[1]/div/div/div/div/div/div[2]/button[1]/div/span/span').click()
    except:
        print('No cookies to accept.')

    # Ir al login
    login_button = driver.find_element(By.XPATH, '/html/body/div/div/div/div[2]/main/div/div/div[1]/div/div/div[3]/div[3]/a/div/span/span')
    action.scroll_to_element(login_button).click(login_button).perform()

    # Email
    time.sleep(2)
    driver.find_element(By.XPATH, '//input[@autocomplete="username"]').send_keys(email)
    driver.find_element(By.XPATH, '//span[text()="Siguiente"]').click()

    # Verificación de nombre de usuario (si lo pide)
    time.sleep(2)
    try:
        driver.find_element(By.XPATH, '//input[@name="text"]').send_keys(username)
        driver.find_element(By.XPATH, '//span[text()="Siguiente"]').click()
    except:
        print('No verificación extra solicitada.')

    # Contraseña
    time.sleep(2)
    driver.find_element(By.XPATH, '//input[@name="password"]').send_keys(password)
    driver.find_element(By.XPATH, '//span[text()="Iniciar sesión"]').click()

# --------- 4. Función para twittear ---------
def post_tweet(driver, tweet_text):
    time.sleep(5)
    tweet_box = driver.find_element(By.XPATH, '//div[@data-testid="tweetTextarea_0"]')
    tweet_box.send_keys(tweet_text)
    time.sleep(1)
    driver.find_element(By.XPATH, '//div[@data-testid="tweetButtonInline"]').click()
    print("✅ Tweet enviado correctamente.")
    time.sleep(5)

# --------- 5. MAIN - Ejecución completa ---------
if __name__ == "__main__":
    # 1. Obtener los precios
    df = get_dollar_prices()

    # 2. Generar el texto para el tweet
    tweet_text = generate_tweet_text(df)

    # 3. Inicializar navegador
    driver = webdriver.Chrome()

    # 4. Login y post usando credenciales del archivo .env
    login_to_x(driver, email=email, username=username, password=password)
    post_tweet(driver, tweet_text)

    # 5. Cerrar navegador
    driver.quit()
