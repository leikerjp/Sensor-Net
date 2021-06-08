import requests
import datetime
import time

data = {
        'data_id' : 1,
        'type' : 'fake_data',
        'value' : 3.14159,
        'ctrlr_id' : None,
        'ctrlr_type' : "BIGD123",
        }

while(True):

    r = requests.post('http://localhost:5000/record_data', json=data)
    if r.status_code != requests.codes.ok:
        print("Error - Exiting" + str(r.status_code))
        exit()

    # If we get a response it's to update our data, so do that
    if r.content:
        respDict = r.json()
        data['ctrlr_id'] = respDict['ctrlr_id']

    time.sleep(1)

    r = requests.post('http://localhost:5000/print_data', json=data)
    if r.status_code != requests.codes.ok:
        print("Error - Exiting" + str(r.status_code))
        exit()

    time.sleep(1)

    data['data_id'] = data['data_id'] + 1
    data['value'] = data['value'] + 0.1
