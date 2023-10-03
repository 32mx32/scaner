from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import random
import os


def DRIVER_INIT():
    random_int = str(random.randint(10, 99))
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("user-agent=Mozilla/7.1 (Macintosh; Intel Mac OS X 12_"+random_int+"_7) AppleWebKit/5"+random_int+".26 (KHTML, like Gecko) Chrome/90.0.1"+random_int+"4	 Safari/578."+random_int+"")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    return driver
