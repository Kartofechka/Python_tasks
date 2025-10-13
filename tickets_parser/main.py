from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

TO_CITY = ''
FROM_CITY = ''
LOGIN = ''
PASSWORD = ''


def setup_driver():
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(), options=options)
    return driver


def autorisation(driver, login, password):
    login_input = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.NAME, "login"))
    )
    login_input.clear()
    login_input.send_keys(login)

    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "password"))
    )
    password_input.clear()
    password_input.send_keys(password)

    dologin = driver.find_element(By.NAME, "dologin")
    driver.execute_script("arguments[0].click();", dologin)


def popup_trash(driver):
    try:
        inform_popup = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "modal-content"))
        )
        close_button = inform_popup.find_element(By.CLASS_NAME, "close.close--black")
        close_button.click()
        time.sleep(1)
    except:
        pass

    try:
        cookies_popup = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "cookies-popup__wrap"))
        )
        close_button = cookies_popup.find_element(By.CLASS_NAME, "cookies-popup__btn")
        close_button.click()
        time.sleep(1)
    except:
        pass


def search_routes(driver, from_city, to_city):
    from_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "from"))
    )
    from_input.clear()
    from_input.send_keys(from_city)

    to_input = driver.find_element(By.NAME, "to")
    to_input.clear()
    to_input.send_keys(to_city)

    search_button = driver.find_element(By.CSS_SELECTOR, ".btn.btn-default.btn-submit.js-input-taber")
    driver.execute_script("arguments[0].click();", search_button)


def print_routes(driver):
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".sch-table__body.js-sort-body"))
    )

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


def search_sit(driver):
    buy_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".btn.btn-index"))
    )
    driver.execute_script("arguments[0].click();", buy_button)

    time.sleep(1)

    click_on_sits = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".pl-accord__cell.cell-1"))
    )
    driver.execute_script("arguments[0].click();", click_on_sits)

    time.sleep(1)

    input_passangers_data = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".btn.btn-index-2"))
    )
    driver.execute_script("arguments[0].click();", input_passangers_data)

    time.sleep(1)


def input_passanger(driver):
    click_in_surname = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "last_name_1"))
    )
    driver.execute_script("arguments[0].click();", click_in_surname)
    time.sleep(1.5)
    input_data = WebDriverWait(driver, 10).until(   
        EC.presence_of_element_located((By.CLASS_NAME, "pass-form__history-link"))
    )
    driver.execute_script("arguments[0].click();", input_data)
    time.sleep(1.5)


def submit_ticket(driver):
    checkbox_visual = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, ".jq-checkbox__div"))
    )
    driver.execute_script("arguments[0].click();", checkbox_visual)


    submit = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".btn.btn-default.info-form__submit"))
    )
    driver.execute_script("arguments[0].click();", submit)


def login_passenger(driver):
    login_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".item_1.cabinet"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", login_button)
    login_button.click()


def buying_ticket(driver, from_city, to_city, login, password):
    driver.get("https://pass.rw.by/ru/")

    time.sleep(5)
    popup_trash(driver)

    time.sleep(2)
    login_passenger(driver)

    time.sleep(3)

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "auth-popup"))
    )

    autorisation(driver, login, password)
    search_routes(driver, from_city, to_city)
    print_routes(driver)
    search_sit(driver)
    input_passanger(driver)
    submit_ticket(driver)

    input('')
    
def main():
    driver = setup_driver()
    buying_ticket(driver, to_city=TO_CITY, from_city=FROM_CITY, login=LOGIN, password=PASSWORD)
    input("")
    driver.quit()


main()

