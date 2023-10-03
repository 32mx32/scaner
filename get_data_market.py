import os
import gspread

import redis
import json
import time



r = redis.Redis(host='localhost', port=6379, db=0)

folder_link = os.path.abspath(os.getcwd())
gc = gspread.service_account(filename = folder_link + '/config/credentials.json')
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1UmQKXgbq0-OGzDrG4PRBobafo6nsuRHbXw0RYswxSVI')
worksheet_list = sh.worksheets()

scan_interval = 5   # интервал сканирования в минутах



def start_scan():
    ignore_worksheet_list = ['Firebase', 'timer']
    for worksheet in worksheet_list:
        worksheet_title = worksheet.title
        if not worksheet_title in ignore_worksheet_list:
            print('сканирование', worksheet_title)
            sellers_price_arr = sh.worksheet(worksheet_title).get_values()
            json_list = json.dumps(sellers_price_arr)
            r.set(worksheet_title, json_list)   # запись в redis
            time.sleep(10)   # чтобы не привысить квоту, подождем немного

def scan_timer():
    while True:
        time.sleep(1)
        local_min = str(time.localtime().tm_min)
        if len(local_min) == 1:
            local_min = '0' + local_min
        if (int(local_min) % scan_interval) == 0:
            start_scan()

scan_timer()
