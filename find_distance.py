import requests
import json
import pandas as pd
# xlrd

key = ''
def make_list_of_plases():
    with open('list_of_hospitals.json') as f:
        list_of_h = json.load(f)
    return  ['{},{}'.format( hospital['lat'], hospital['lng']) for hospital in list_of_h]



def find_nearest_hospital(data):
    value = int(data['rows'][0]['elements'][0]['duration']['value'])
    result = {'hospital': data['destination_addresses'][0],
            'distance': data['rows'][0]['elements'][0]['distance'],
            'duration': data['rows'][0]['elements'][0]['duration']}
    for hospital, info in zip(data['destination_addresses'], data['rows'][0]['elements']):
        if int(info['duration']['value']) < value:
            value = int(info['duration']['value'])
            result = {'hospital': hospital,
                    'distance': info['distance'],
                    'duration': info['duration']}
    return result



# вот тут можно подкрутить параметры для настройки
body = {
    'key': key,
    'origins': 'Maskavas iela 273',
    'units': 'imperial',
    'destinations': '|'.join(make_list_of_plases())
}

#от этого числа зависит сколько запросов будет сделано за один скрипт,не забудь прочекать лимиты для текущего ключа!!!!!!!!!
number_of_addresses_for_requests = 1




df = pd.read_excel('Adresa_kvartir.xlsx').fillna('')
undefined_data = df.index[df['Distance Text'] == ''].tolist()

for row in range(number_of_addresses_for_requests):
    body['origins']=df['Address'][undefined_data[row]]
    response = requests.get(
        url='https://maps.googleapis.com/maps/api/distancematrix/json', params=body)
    data = json.loads(response.content.decode())
    hospital = find_nearest_hospital(data)
    df['Distance Text'][undefined_data[row]] = hospital['distance']['text']
    df['Distance Value'][undefined_data[row]] = hospital['distance']['value']
    df['Duration Text'][undefined_data[row]] = hospital['duration']['text']
    df['Duration Value'][undefined_data[row]] = hospital['duration']['value']

df.to_excel('Adresa_kvartir.xlsx', index = False)
