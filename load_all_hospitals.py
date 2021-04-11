import requests
import json

key = 'AIzaSyABvBEFYZPUNzdLENdZg8Jwb_O61XCc_-I'

# вот тут ищет все больницы в окрестностях риги б можно поменять тип, и еще вставить всякие штуки типа поиска по ключевому слову
body = {'key': key,
        'location': '56.950000, 24.110000',
        'radius': '15000',
        'type': 'hospital'}
list_of_all_hospitals = []


def store_all_data(results):
    for address in results:
        location = {

            'lat': address['geometry']['location']['lat'],
            'lng': address['geometry']['location']['lng'],
            'name': address['name']

                }
        list_of_all_hospitals.append(location)


while True:
    response = requests.get(
        url='https://maps.googleapis.com/maps/api/place/nearbysearch/json', params=body)

    data = json.loads(response.content.decode())
    store_all_data(data['results'])

    next_page = data.get('next_page_token')
    if next_page:
        body['pagetoken']= next_page
    else:
        break

with open('list_of_hospitals_test.json', 'w') as f:
  f.write(json.dumps(list_of_all_hospitals))

