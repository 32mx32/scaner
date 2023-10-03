from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC

from functions.driver_init import DRIVER_INIT



def GET_DATA_PAGE(seller_link_dict, wait_element):
    page_list = ''
    for link in seller_link_dict:
        try:
            print(link)
            driver = DRIVER_INIT()
            driver.get(link)
            wait(driver, 20).until(EC.visibility_of_element_located(wait_element))
            page = driver.page_source
            page_list = page_list + page
        except:
            print(link, 'error')
            pass
    soup = BeautifulSoup(page_list, 'html.parser')
    driver.close()
    return soup
