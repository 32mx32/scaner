import time

def GET_CURRENT_TIME():
    current_time = time.localtime(time.time())
    now_time = time.strftime("%d.%m.%Y %H:%M", current_time)    
    return now_time