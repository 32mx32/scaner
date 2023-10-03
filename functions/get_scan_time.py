from datetime import date, datetime, timedelta

def GET_SCAN_TIME(worksheet_timer_page):
    # worksheet_start_scan_hour:worksheet_start_scan_minute - время сканирования, устанавливается в таблице
    worksheet_start_scan_cell = worksheet_timer_page.find('START_SCAN')
    worksheet_start_scan_hour = int(worksheet_timer_page.cell(worksheet_start_scan_cell.row + 1, worksheet_start_scan_cell.col).value.replace(' ', '').replace('часов', ''))
    worksheet_start_scan_minute = int(worksheet_timer_page.cell(worksheet_start_scan_cell.row + 1, worksheet_start_scan_cell.col + 1).value.replace(' ', '').replace('минут', ''))
    # worksheet_interval_scan - интервал между сканированием, устанавливается в таблицк
    worksheet_interval_scan_cell = worksheet_timer_page.find('INTERVAL')
    worksheet_interval_scan = int(worksheet_timer_page.cell(worksheet_interval_scan_cell.row + 1, worksheet_interval_scan_cell.col).value.replace(' ', '').replace('минут', ''))
    # массив для временных меток начала сканирования
    scan_time_arr = []
    # в сутках 1440 минут
    for item in range(0, 1440, worksheet_interval_scan):
        # прибавляет к времени начала сканирования заданный интервал, переводит в строку и убираем лишнее
        scan_time_label = (str(timedelta(hours=worksheet_start_scan_hour, minutes=worksheet_start_scan_minute) + timedelta(minutes=item))).replace(' ', '').replace('1day,', '')[:-3]
        # добавляет 0 в начало, если время без 0 в начале)))
        if len(scan_time_label) < 5:
            scan_time_label = '0' + scan_time_label
        scan_time_arr.append(scan_time_label)
    return scan_time_arr