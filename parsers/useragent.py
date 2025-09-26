from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

user_agent = "PotatoPC/777.0 (iPotato; CPU KartoshkaForce 4080Ti UltraProMax)"
options = Options()
options.add_argument(f"user-agent={user_agent}")

driver = webdriver.Chrome(service=Service(), options=options)

driver.get("https://www.whatismybrowser.com/detect/what-is-my-user-agent")

input()


