import os
import gspread

import redis
import json
import time



# r = redis.Redis(host='localhost', port=6379, db=0)

folder_link = os.path.abspath(os.getcwd())
gc = gspread.service_account(filename = folder_link + '/config/credentials.json')
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1oTL_yqk1hjMeN8w3pMFAprRw6QuNbJCLV6b2b_5mX8U')
# worksheet_list = sh.worksheets()

scan_interval = 5   # интервал сканирования в минутах


worksheet_title = 'iphone'
sellers_price_arr = sh.worksheet(worksheet_title.lower()).get_values()


def GET_SERVICE_DATA(sellers_price_arr):
    model_row = sellers_price_arr[0]
    seller_row = sellers_price_arr[1]   # строка с именами селлеров
    seller_index_arr = []               # индексы селлеров со статусом TRUE
    service_price_dict = {}
    for index, worksheet_seller_name in enumerate(seller_row):
        if worksheet_seller_name == 'site':
            seller_index_arr.append(index)
            #
            count = index
            for item in range(10, 1, -1):
                worksheet_model_name = model_row[count]
                if worksheet_model_name == '':
                    count = count - 1
                    pass
                else:
                    # print(count, worksheet_model_name)
                    # print(index, worksheet_seller_name)
                    model_price_dict = {}
                    for index_row, row in enumerate(sellers_price_arr):
                        # print(index_row, row)
                        # print()
                        worksheet_service_name = row[0]
                        if worksheet_service_name != '' and index_row != 0 and index_row != 1 :
                            worksheet_service_price = sellers_price_arr[index_row][index]
                            service_name_dict = {}
                            # if worksheet_service_price != '':
                            if worksheet_service_price:
                                print(worksheet_model_name, worksheet_service_price)
                                worksheet_service_info = sellers_price_arr[index_row][1]
                                worksheet_service_time = sellers_price_arr[index_row][2]
                                worksheet_service_sale = sellers_price_arr[index_row][3]
                                worksheet_service_work = sellers_price_arr[index_row][index + 1]
                                worksheet_service_part = sellers_price_arr[index_row][index + 2]
                                service_name_dict.update(
                                    {
                                        'service_model' : worksheet_model_name,
                                        'service_price' : worksheet_service_price,
                                        'service_name'  : worksheet_service_name,
                                        'service_info'  : worksheet_service_info,
                                        'service_time'  : worksheet_service_time,
                                        'service_sale'  : worksheet_service_sale,
                                        'service_work'  : worksheet_service_work,
                                        'service_part'  : worksheet_service_part,
                                        'service_row'   : index_row,
                                        'service_col'   : index
                                    }
                                )
                                model_price_dict.update({worksheet_service_name : service_name_dict})
                            # print(index_row, worksheet_service_name, worksheet_service_price)
                    if model_price_dict:
                        service_price_dict.update({worksheet_model_name : model_price_dict})
                    break
    print(service_price_dict)
    return service_price_dict

GET_SERVICE_DATA(sellers_price_arr)
