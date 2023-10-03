from config.config import WORKESHEET_COL_NAME
import re



worksheet_col_name = WORKESHEET_COL_NAME

def GET_WRITABLE_ARR(service_price_dict, worksheet_title, seller, sh):
    print(service_price_dict)
    worksheet = sh.worksheet(worksheet_title)
    worksheet_model_row = worksheet.row_values(1)
    worksheet_seller_row = worksheet.row_values(2)
    worksheet_service_col = worksheet.col_values(1)
    arr = []
    # удаление лишнего из названий услуг
    for i, worksheet_service_name in enumerate(worksheet_service_col):
        if worksheet_service_name:
            worksheet_service_name = re.sub(r'\W', '', worksheet_service_name.lower())
            worksheet_service_col[i] = worksheet_service_name
    # поиск адреса модель/селлер, формирование и запись массива в таблицу
    for site_model_name in service_price_dict: # перебор моделей в списке с услугами, полученного парсером с сайта
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        # поиск адреса модель/селлер
        # нужно взять все что есть в первой строке и это будет название моделей
        # которое занимает некоторое количеством столбцов и с продавцами под ним
        for item, worksheet_model_name in enumerate(worksheet_model_row):
            worksheet_model_name = re.sub(r'\W', '', worksheet_model_name.lower())
            # print(' ==== >>> worksheet_model_name == site_model_name', worksheet_model_name, site_model_name)
            if worksheet_model_name == site_model_name:
                # print('worksheet_model_name == site_model_name', worksheet_model_name, site_model_name)
                # print(f'\nначало зоны {site_model_name} столбец {worksheet_col_name[item] + str(1)}\n')
                # затпм опуститья на строку ниже и найти селлера
                for num in range(item, len(worksheet_seller_row)):
                    if worksheet_seller_row[num] == seller:
                        # print(f'\nискомый селлер {seller} для модели {site_model_name}, находится в ячейке {worksheet_col_name[num] + str(2)}\n')
                        write_in_sheet_range_start = worksheet_col_name[num] + str(3)   # начало записи столбца
                        write_in_sheet_range_end = worksheet_col_name[num] + str(len(worksheet_service_col)) # конец записи столбца
                        break
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        # формирует выходной упорядоченый масссив с ценами для записи в таблицу
        worksheet_service_arr = [] # для сбора только непустых строчек
        for item, service_name in enumerate(worksheet_service_col):
            if item == 0 or item == 1:
                continue
            if service_name:
                worksheet_service_arr.append(service_name)
        result_arr = []
        for item, worksheet_service_name in enumerate(worksheet_service_arr):
            result_arr.append([' '])
            for site_service_name in service_price_dict[site_model_name]:
                if worksheet_service_name == site_service_name:
                    result_arr[item] = [service_price_dict[site_model_name][site_service_name]]
        write_in_sheet_range = f'{write_in_sheet_range_start}:{write_in_sheet_range_end}'
        arr.append({'range' : write_in_sheet_range, 'values' : result_arr}) # список для записи 
        # print(arr)
    worksheet.batch_update(arr)