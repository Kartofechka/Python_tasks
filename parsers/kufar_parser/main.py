from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

def setup_driver():
    service = Service()
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def get_products(driver, url):
    driver.get(url)

    with open("products.csv", mode="w", encoding='utf-8', newline='') as w_file:
        file_writer = csv.writer(w_file, delimiter="|")
        file_writer.writerow(["Название", "Стоимость", "Размер", "Местоположение", "Дата публикации", "Ссылка"])

        while True:
            WebDriverWait(driver, 15).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-testid='kufar-ad']"))
            )
            cards = driver.find_elements(By.CSS_SELECTOR, "[data-testid='kufar-ad']")

            for card in cards:
                try:
                    name = card.find_element(By.CSS_SELECTOR, "h3.styles_title__FL3dv").text
                    price = card.find_element(By.CSS_SELECTOR, "p.styles_price__aVxZc span").text
                    size = card.find_element(By.CSS_SELECTOR, "p.styles_parameters__UiU_l").text
                    location = card.find_element(By.CSS_SELECTOR, "div.styles_secondary__0nTZT p:nth-of-type(2)").text
                    date = card.find_element(By.CSS_SELECTOR, "div.styles_secondary__0nTZT span").text
                    link = card.get_attribute("href")
                    file_writer.writerow([name, price, size, location, date, link])
                except Exception as e:
                    continue

            try:
                next_btn = driver.find_element(By.CSS_SELECTOR, "[data-testid='generalist-pagination-next-link']")
                if "styles_disable__kbC6l" in next_btn.get_attribute("class"):
                    break
                driver.execute_script("arguments[0].scrollIntoView(true);", next_btn)
                driver.execute_script("arguments[0].click();", next_btn)
                time.sleep(3)
            except Exception as e:
                break


driver = webdriver.Chrome(service=Service(), options=Options())
URL = "https://www.kufar.by/l/muzhskaya-verhnyaya-odezhda/m~palto/winter/w~chernyj?sort=lst.d"

get_products(driver, url=URL)

input()
driver.quit()