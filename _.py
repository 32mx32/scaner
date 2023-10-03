service_replace_dict = {
    'applepro' : {
        'macbook' : {
            'pro16a27802023m2' : ['macbookpro16m2'],
            'заменаматрицыотдельно' : [
                'заменаматрицыmacbookpro13retinam2',
                'заменаматрицыpro14a27792023m2',
                'заменаматрицыmacbookpro14m2',
                'заменаматрицыmacbookpro16a2780',
                'заменаматрицыlcdpro17a1229a1261a129720072011',
            ]
        },
    }
}

find_word = 'macbookpro16m2'

for key in service_replace_dict['applepro']['macbook']:
    if find_word in service_replace_dict['applepro']['macbook'][key]:
        print(key)


# model_name = model_name.replace(word, replace_dict[worksheet_title][word])
