from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

def setup_driver():
    service = Service()
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def open_page(driver, url):
    driver.get(url)
    time.sleep(2)

def get_products(driver):
    proxies = []
    rows = driver.find_elements(By.CLASS_NAME, "odd")
    for row in rows:
        columns = row.text.strip().split()
        if len(columns) >= 4:
            ip = columns[0]
            port = columns[1]
            anonymity = columns[3].lower()
            https = columns[4].lower()
            if "anonymous" in anonymity and "yes" in https:
                proxy_data = ip + ':' + port
                proxies.append(proxy_data)
    return proxies

def pars_proxies(base_url):
    driver = setup_driver()
    open_page(driver, base_url)
    time.sleep(2)
    proxy = get_products(driver)[0]
    driver.quit()
    print(proxy)
    return proxy

proxy = pars_proxies("https://freeproxylist.cc/servers/")
user_agent = "PotatoPC/777.0 (iPotato; CPU KartoshkaForce 4080Ti UltraProMax)"

options = Options()
options.add_argument(f"--proxy-server={proxy}")
options.add_argument(f"user-agent={user_agent}")

driver = webdriver.Chrome(service=Service(), options=options)
driver.get("https://2ip.ru/")

input()
driver.quit()


