from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

def setup_driver():
    service = Service()
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def open_page(driver, url):
    driver.get(url)
    time.sleep(2)

def hide_cookie(driver):
    try:
        driver.execute_script("document.getElementById('cookies-informer').style.display = 'none';")
    except:
        pass

def get_products(driver):
    products = driver.find_elements(By.CLASS_NAME, "prod__link")
    for product in products:
        name = product.text.strip()
        link = product.get_attribute("href")
        print(f"Название: {name}, ссылка - {link}")

def go_to_next_page(driver):
    next_buttons = driver.find_elements(By.CSS_SELECTOR, "a.paging__next")
    if not next_buttons:
        return False
    next_button = next_buttons[0]
    driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
    time.sleep(1)
    next_button.click()
    return True

def pars_all_pages(base_url):
    driver = setup_driver()
    open_page(driver, base_url)
    page = 1

    while True:
        print(f"\nСтраница {page}")
        time.sleep(2)
        hide_cookie(driver)
        get_products(driver)
        if not go_to_next_page(driver):
            print("Последняя страница достигнута.")
            break
        page += 1

    driver.quit()

pars_all_pages("https://home.1k.by/kitchen-electriccookers/")
