import requests
import json
import pandas as pd

# xlrd

key = ''

# от этого числа зависит сколько запросов будет сделано за один скрипт,не забудь прочекать лимиты для текущего ключа!!!!!!!!!
number_of_addresses_for_requests = 4

df = pd.read_excel('Adresa_kvartir.xlsx').fillna('')
undefined_data = df.index[df['Lat,Lng'] == ''].tolist()

for row in range(number_of_addresses_for_requests):
    addressLine = df['Address'][undefined_data[row]]+", Riga"
    response = requests.get(
        url='http://dev.virtualearth.net/REST/v1/Locations?countryRegion=LT&locality=Riga&addressLine={addressLine}&maxResults=1&key={key}'.format(key=key, addressLine=addressLine))
    data = json.loads(response.content.decode())
    df['Lat,Lng'][undefined_data[row]]= '{},{}'.format(*data['resourceSets'][0]['resources'][0]['point']['coordinates'])


df.to_excel('Adresa_kvartir.xlsx', index=False)
