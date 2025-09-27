from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def setup_driver():
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(), options=options)
    return driver

def search_routes(driver, from_city, to_city):
    driver.get("https://pass.rw.by/ru/")

    wait = WebDriverWait(driver, 15)

    from_input = wait.until(EC.presence_of_element_located((By.NAME, "from")))
    from_input.clear()
    from_input.send_keys(from_city)


    to_input = driver.find_element(By.NAME, "to")
    to_input.clear()
    to_input.send_keys(to_city)


    # Закрытие cookies
    try:
        cookies_popup = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "cookies-popup__wrap"))
        )
        close_button = cookies_popup.find_element(By.CLASS_NAME, "cookies-popup__btn")
        close_button.click()
        time.sleep(1)
    except:
        pass

    search_button = driver.find_element(By.CSS_SELECTOR, ".btn.btn-default.btn-submit.js-input-taber")
    driver.execute_script("arguments[0].click();", search_button)

    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".sch-table__body.js-sort-body")))

    rows = driver.find_elements(By.CSS_SELECTOR, ".sch-table__row")

    print(f"\nНайденые поезда:\n")
    for row in rows:
        try:
            train_number = row.find_element(By.CSS_SELECTOR, ".train-number").text
            train_name = row.find_element(By.CSS_SELECTOR, ".train-route").text
            departure = row.find_element(By.CSS_SELECTOR, ".sch-table__time.train-from-time").text
            arrival = row.find_element(By.CSS_SELECTOR, ".sch-table__time.train-to-time").text
            duration = row.find_element(By.CSS_SELECTOR, ".sch-table__duration.train-duration-time").text
            if (train_number != ""):
                print(f"{train_number} | {train_name} | Отправление: {departure} | Прибытие: {arrival} | В пути: {duration}")
        except:
            continue

    buy_button = driver.find_element(By.CSS_SELECTOR, ".btn.btn-index")
    driver.execute_script("arguments[0].click();", buy_button)

def main():
    driver = setup_driver()
    search_routes(driver, "Минск", "Лида")
    input("")
    driver.quit()

main()
