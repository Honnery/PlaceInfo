import requests
import json
import pandas as pd

# xlrd

key = ''
with open('list_of_hospitals.json') as f:
    list_of_h = json.load(f)
def make_list_of_plases():
    return [{'latitude': hospital['lat'], 'longitude': hospital['lng']} for hospital in list_of_h]


list_of_places = make_list_of_plases()

def find_nearest_hospital(data):
    value = int(data['resourceSets'][0]['resources'][0]['results'][0]['travelDistance'])
    result = {'hospital': list_of_h[0]['name'],
              'distance': data['resourceSets'][0]['resources'][0]['results'][0]['travelDistance'],
              'duration': data['resourceSets'][0]['resources'][0]['results'][0]['travelDuration']}
    for index, info in enumerate(data['resourceSets'][0]['resources'][0]['results']):
        if int(info['travelDuration']) < value:
            value = int(info['travelDuration'])
            result = {'hospital': list_of_h[index]['name'],
                      'distance': info['travelDistance'],
                      'duration': info['travelDuration']}
    return result




# вот тут можно подкрутить параметры для настройки
body = {
    "destinations": list_of_places,
    "travelMode": "driving"
}

# от этого числа зависит сколько запросов будет сделано за один скрипт,не забудь прочекать лимиты для текущего ключа!!!!!!!!!
number_of_addresses_for_requests = 2

df = pd.read_excel('Adresa_kvartir.xlsx').fillna('')
undefined_data = df.index[df['Distance Value'] == ''].tolist()

for row in range(number_of_addresses_for_requests):
    addressco = df['Lat,Lng'][undefined_data[row]]
    body['origins'] = [

        {
            "latitude": addressco.split(',')[0],
            "longitude": addressco.split(',')[1],

         }
    ]
    response = requests.post(
        url='https://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix?key={}'.format(key), json=body)
    data = json.loads(response.content.decode())
    hospital = find_nearest_hospital(data)
    df['Distance Value'][undefined_data[row]] = hospital['distance']
    df['Duration Value'][undefined_data[row]] = hospital['duration']

df.to_excel('Adresa_kvartir.xlsx', index=False)
