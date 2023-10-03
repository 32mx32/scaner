from config.config import WORKESHEET_COL_NAME

from datetime import date, datetime, timedelta
import tzlocal
import time
import re



worksheet_col_name = WORKESHEET_COL_NAME

def GET_WRITABLE_ARR(site_models_dict, seller, worksheet_title, sh):
    worksheet = sh.worksheet(worksheet_title)
    worksheet_models_col = worksheet.col_values(1)
    worksheet_sellers_names = worksheet.row_values(1)    
    #
    for worksheet_seller_name in worksheet_sellers_names:
        if seller.lower() == worksheet_seller_name.lower():
            start_write_col = worksheet.find(worksheet_seller_name).col
    #
    worksheet_models_arr = []
    for i, worksheet_parts_name in enumerate(worksheet_models_col):
        if worksheet_parts_name:
            worksheet_parts_name = re.sub(r'\W', '', worksheet_parts_name.lower())
            # worksheet_parts_name = worksheet_parts_name.replace('iphone', '')
            worksheet_models_arr.append(worksheet_parts_name)
        else:
            start_write_row = i + 2
    # print(worksheet_models_arr)
    #    формирует выходной упорядоченый масссив с ценами для записи в таблицу
    result_arr = []
    for i, worksheet_model_name in enumerate(worksheet_models_arr):
        result_arr.append([' '])
        for parts_name in site_models_dict:
            # print(worksheet_parts_name, parts_name)
            if parts_name == worksheet_model_name:
                result_arr[i] = [site_models_dict[parts_name]]
    print('массив для записи --> \n', result_arr)
    print()
    val_range_one = str(worksheet_col_name[start_write_col - 1]) + str(start_write_row)    # первое значение для записи диапазона range / B2
    val_range_two = str(worksheet_col_name[start_write_col - 1]) + str(len(result_arr) + start_write_row)    # второе значение для записи диапазона range / B8
    range_write = val_range_one + ':' + val_range_two
    print(range_write)
    worksheet.batch_update(
        [
            {'range': range_write, 'values': result_arr}
        ]
    )
    date = datetime.now(tzlocal.get_localzone()).strftime("%d-%m-%Y %H:%M")   
    worksheet.update_cell(start_write_row - 2, start_write_col, date)  
    time.sleep(5)
    