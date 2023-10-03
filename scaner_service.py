from dictionary.dictionary_service import service_link_dict, service_replace_dict
from dictionary.dict_service import service_link_dictionary, service_replace_dictionary
from config.config import SHEET_FOR_SERVICE

from functions.get_current_time import GET_CURRENT_TIME
from functions.get_scan_time import GET_SCAN_TIME
from functions.get_data_page import GET_DATA_PAGE
from functions.driver_init import DRIVER_INIT
from functions.get_write_arr_service import GET_WRITABLE_ARR

from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import re



sh = SHEET_FOR_SERVICE
worksheet_list = sh.worksheets()



# ищет в словаре значения и возврашает ключ словаря для этого значения
def FIND_REPLACE_KEY(replace_dict, worksheet_title, find_word):
    for key in replace_dict[worksheet_title]:
        if find_word in replace_dict[worksheet_title][key]:
            return key

def REPLACE_WORD(replace_dict, worksheet_title, service_name):
    for key in replace_dict[worksheet_title]:
        for word in replace_dict[worksheet_title][key]:
            service_name = service_name.replace(word, key)
            return service_name



def HOUSE(worksheet_title):    
    link_dict = service_link_dict['house']
    replace_dict = service_replace_dict['house']
    #
    wait_element = By.CLASS_NAME, 'modal-price'
    soup = GET_DATA_PAGE(link_dict[worksheet_title], wait_element)
    service_price_dict = {}
    ads = soup.find_all('div', 'modal-price')
    for ad in ads:
        model_name = ad.find('p', 'h1').text.strip().lower()
        model_name = re.sub(r'\W', '', model_name)
        # print(model_name)
        for word in replace_dict[worksheet_title]:
            model_name = model_name.replace(word, replace_dict[worksheet_title][word])
        service_list = ad.find_all('div', 'row')
        print('model_name *----->', model_name)
        model_price_dict = {}
        for service_block in service_list:
            service_name = service_block.find('p', 'col').text.strip()
            service_name = re.sub(r'\W', '', service_name.lower())
            for word in replace_dict[worksheet_title]:
                service_name = service_name.replace(word, replace_dict[worksheet_title][word])
            service_price = service_block.find('p', 'col-5').text.strip().replace('₽', '').replace(' ', '').replace('.', '').replace('Бесплатно', '-').replace('Позапросу', '-')
            print(service_name, service_price)
            model_price_dict.update({service_name : service_price})
        service_price_dict.update({model_name : model_price_dict})
    GET_WRITABLE_ARR(service_price_dict, worksheet_title, seller='house', sh=sh) 
    
def MOBI(worksheet_title):
    link_dict = service_link_dict['mobi']
    replace_dict = service_replace_dict['mobi']
    
    
    driver = DRIVER_INIT()
    driver.implicitly_wait(10)
    driver.maximize_window()
    driver.get('https://mobi-service.com')
    
    
    # уберем эти блоки со страницы style.display = 'none'
    box_zag = driver.find_element(By.CLASS_NAME, 'box_zag')
    box_search = driver.find_element(By.CLASS_NAME, 'box_search.kv_catalog_search')
    bg1 = driver.find_element(By.ID, 'bg1')
    driver.execute_script("arguments[0].style.display = 'none';", box_zag)
    driver.execute_script("arguments[0].style.display = 'none';", box_search)
    driver.execute_script("arguments[0].style.display = 'none';", bg1)
    
    element = 'iPhone'
    device_select = driver.find_element(By.ID, 'kv_catalog').find_element(By.XPATH, f"//button[@data-id='{element}']")
    device_select.click()
        
        
    page_list = ''
    for item in link_dict[worksheet_title]:
        select_model = driver.find_element(By.XPATH, f"//button[@data-search='{item}']")
        select_model.click()
        time.sleep(1)
        driver.execute_script("window.scrollTo(document.body.scrollHeight, 0);")
        print(select_model.text)
        page = driver.page_source
        page_list = page_list + page
    soup = BeautifulSoup(page_list, 'html.parser')
    driver.close()
    
        
    service_price_dict = {}
    ads = soup.find_all('div', 'box_service active')
    for ad in ads:
        model_name = ad.find('div', 'box_left box_zag').find('h3').text.strip().lower().replace(' ', '').replace('ремонт', '').replace('iphone', '')
        model_name = re.sub(r'\W', '', model_name)
        model_name = model_name.replace('8se2020', '8').replace('1212pro', '12')
        # print(model_name)
        #
        model_price_dict = {}
        service_list = ad.find_all('div', 'box_row')
        for item in service_list:
            service_name = item.find('h6').text.strip().lower()
            service_name = re.sub(r'\W', '', service_name)
            for word in replace_dict[worksheet_title]:
                service_name = service_name.replace(word, replace_dict[worksheet_title][word])
            #
            service_price = item.find('span', 'price').text.strip().lower().replace(' ', '').replace('руб.', '').replace('бесплатно', '-').replace('позапросу', '-')
            service_price = re.sub(r'\W', '', service_price)
            #
            # print(service_name, service_price)
            #
            model_price_dict.update({service_name : service_price})
        service_price_dict.update({model_name : model_price_dict})
    GET_WRITABLE_ARR(service_price_dict, worksheet_title, seller='mobi', sh=sh)

def APPLEPRO(worksheet_title):
    link_dict = service_link_dictionary['applepro']
    replace_dict = service_replace_dictionary['applepro']
    #
    wait_element = By.CSS_SELECTOR, 'div.table-wrap'
    soup = GET_DATA_PAGE(link_dict[worksheet_title], wait_element)
    #
    service_price_dict = {}
    ads = soup.find_all('div', {'id': 'main'})
    for ad in ads:
        model_name = ad.find('div', {'id': 'bx_breadcrumb_2'}).text.strip().lower()
        model_name = model_name.replace('ремонт' , '').replace('iphone', '').replace('se 3 (2022)', 'se2022')
        model_name = re.sub(r'\W', '', model_name)
        #
        for key in replace_dict[worksheet_title]:
            for word in replace_dict[worksheet_title][key]:
                model_name = model_name.replace(word, key).replace(' ', '').lower() # в словаре могут быть пробелы и капс!!!
        # 
        print('model_name *----->', model_name)
        #
        service_list = ad.find('table').find_all('tr')
        model_price_dict = {}
        for item in service_list:
            if item.find('td', 'col1'):
                service_name = item.find('td', 'col1').find('span').text.strip().lower()
                service_name = re.sub(r'\W', '', service_name)
                # 
                for key in replace_dict[worksheet_title]:
                    for word in replace_dict[worksheet_title][key]:
                        service_name = service_name.replace(word, key).replace(' ', '').lower() # в словаре могут быть пробелы и капс!!!
                #
                service_price = item.find('td', 'col2').text.strip().lower()
                service_price = service_price.replace('записаться', '').replace('р', '').replace(' ', '')
                # service_price = re.sub(r'\W', '', service_price)
                if len(service_price) > 6:
                    for i, letter in enumerate(service_price):
                        if letter == 'д':
                            service_price = service_price[:i]
                    # service_price_old = service_price[:(len(service_price)/2)]
                    # service_price_new = service_price[:-(len(service_price)/2)]
                    # print(service_price_old, '/', service_price_new)
                # if service_name == 'диагностика':
                #     service_price = '-'
                print(service_name, service_price)
                model_price_dict.update({service_name : service_price})
        service_price_dict.update({model_name : model_price_dict})  
    GET_WRITABLE_ARR(service_price_dict, worksheet_title, seller='applepro', sh=sh) 
           
def WOAP(worksheet_title):
    link_dict = service_link_dict['woap']
    replace_dict = service_replace_dict['woap']
    #
    wait_element = By.CSS_SELECTOR, 'div.view-content'
    soup = GET_DATA_PAGE(link_dict[worksheet_title], wait_element)
    #
    component_price_dict = {}
    ads = soup.find_all('section', 'col-sm-9')
    for ad in ads:
        model_name = ad.find('h1' , 'page-header').text.strip().lower().replace('запчасти', '').replace('iphone', '')
        model_name = re.sub(r'\W', '', model_name)
        for word in replace_dict[worksheet_title]:
            model_name = model_name.replace(word, replace_dict[worksheet_title][word])
        content_block = ad.find_all('div', 'product-row')
        print(f'\nmodel_name---> {model_name}\n')
        model_price_dict = {}
        for content in content_block:
            component_name = content.find('div', 'field-item odd').text.strip().lower()
            component_name = re.sub(r'\W', '', component_name)
            for word in replace_dict[worksheet_title]:
                component_name = component_name.replace(word, replace_dict[worksheet_title][word])
            #
            component_price = content.find('span', 'uc-price').text.strip().lower().replace('руб', '')
            component_price = re.sub(r'\W', '', component_price)
            #
            model_price_dict.update({component_name : component_price})
            print('*----->', component_name, component_price)
            # print(component_name, component_price)
        component_price_dict.update({model_name : model_price_dict})
        #
    GET_WRITABLE_ARR(component_price_dict, worksheet_title, seller='woap', sh=sh) 
    
    
    
def START_SCAN():
    scan_dict = {
        'iphone' :  {
            'APPLEPRO'  : APPLEPRO,
            'MOBI'      : MOBI,
            'HOUSE'     : HOUSE,
            'WOAP'      : WOAP
                },
        'macbook': {
            'APPLEPRO'  : APPLEPRO,
            'HOUSE'     : HOUSE,
            'WOAP'      : WOAP
            },
        'watch' : {
            'APPLEPRO'  : APPLEPRO,
            'HOUSE'     : HOUSE,
            'WOAP'      : WOAP
        },
        'ipad' : {
            'APPLEPRO'  : APPLEPRO,
            'HOUSE'     : HOUSE,
            'WOAP'      : WOAP   
        }
    }
    #
    status_cell_row = 1
    status_cell_col = 1
    for worksheet in worksheet_list:
        try:
            if worksheet.title in scan_dict.keys():
                status_str = ''
                try:
                    for seller in scan_dict[worksheet.title]:
                        print(f'*-------> {worksheet.title} {seller} \n')
                        worksheet.update_cell(status_cell_row, status_cell_col, f'{seller} SCAN')
                        worksheet.update_cell(status_cell_row + 1, status_cell_col, f'{GET_CURRENT_TIME()}')
                        scan_function = scan_dict[worksheet.title][seller]
                        scan_function(worksheet.title)
                        #
                        status_str += f'{seller}:SUS  ' 
                except:
                    status_str += f'{seller}:ERR '
                    worksheet.update_cell(status_cell_row, status_cell_col, 'ОШИБКА СКАНИРОВАНИЯ ТЕКУЩЕГО ЛИСТА')
                    pass
                worksheet.update_cell(status_cell_row, status_cell_col, f'{status_str}')
                worksheet.update_cell(status_cell_row + 1, status_cell_col, f'{GET_CURRENT_TIME()}')
            else:
                pass
        except:
            print('ОБЩАЯ ОШИБКА')
            worksheet.update_cell(status_cell_row, status_cell_col, f'{GET_CURRENT_TIME()} ОБЩАЯ ОШИБКА')

def TIMER():
    worksheet_timer_page = sh.worksheet('timer')    # страница, на которой расположены ячейки с таймером
    scan_interval = 30  # scan_interval - время между опросами таблицы
    status_cell = worksheet_timer_page.find('STATUS')
    while True:
        time.sleep(.1)
        local_sec = time.strftime("%S", time.localtime(time.time()))
        if (int(local_sec) % scan_interval) == 0 :  # если прошло scan_interval, обновить время в таблице и проверить, не пора ли начать сканирование
            local_time = time.strftime("%H:%M", time.localtime(time.time()))
            # print(local_time)
            worksheet_timer_page.update_cell(status_cell.row + 1, status_cell.col, (local_time + ':' + str(local_sec))) # вывод локального времени сервереа в таблицу, в ячейку STATUS
            #
            # получает массив с временными метками | получается что делается опрос таблицы каждые scan_interval секунд
            # и каждый раз получает обновленные данные, если вдруг пользователь обновил время и интервал сканирования
            scan_time_arr = GET_SCAN_TIME(worksheet_timer_page)
            print(scan_time_arr)
            #
            for scan_marker in scan_time_arr:
                # print(scan_marker, local_time)
                if scan_marker == local_time:   # не пора ли начать сканирование?
                    print(local_time, 'START')
                    worksheet_timer_page.update_cell(status_cell.row + 1, status_cell.col, 'SCAN')
                    # - * - * - * - * - * - * - * - * - * - * - * - * -
                    # - * - * - * - * - * - * - * - * - * - * - * - * -
                    # - * - * - * - * - * - * - * - * - * - * - * - * -
                    print('\n- * - * - * - * - * - * - * - * - * - * - * - * - START_SCAN  - * - * - * - * - * - * - * - * - * - * - * - * -\n')
                    START_SCAN()
                    print('\n- * - * - * - * - * - * - * - * - * - * - * - * - FINISH_SCAN - * - * - * - * - * - * - * - * - * - * - * - * -\n')
                    # запись в redis
                    # worksheet_title = worksheet.title
                    # sellers_price_arr = sh.worksheet(worksheet_title).get_values()
                    # json_list = json.dumps(sellers_price_arr)
                    # r.set(worksheet_title, json_list)
                    # unpacked_list = json.loads(r.get(worksheet_title))
                    # print('unpacked_list --->', unpacked_list)
                    time.sleep(20)
                    # - * - * - * - * - * - * - * - * - * - * - * - * -
                    # - * - * - * - * - * - * - * - * - * - * - * - * -
                    # - * - * - * - * - * - * - * - * - * - * - * - * -
                    # если сканирование завершится ошибкой и время старта скана не прошло, а ошибка уже появилась
                    # когда по плату должно быть сканирование, но оно уже закончилось
                    while scan_marker == local_time:
                        time.sleep(.1)
                        worksheet_timer_page.update_cell(status_cell.row + 1, status_cell.col, 'WAIT')
                        local_time = time.strftime("%H:%M", time.localtime(time.time()))
                        time.sleep(10)
                        print('pause')



APPLEPRO('iphone')
# HOUSE('ipad')
# MOBI('iphone')
# WOAP('ipad')
# START_SCAN()

# TIMER()
