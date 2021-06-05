import requests
import datetime
import time

data = {
        'data_id' : 1,
        'type' : 'fake_data',
        'value' : 3.14159,
        'ctrlr_id' : 266
        }

while(True):

    r = requests.post('http://localhost:5000/log_data', json=data)
    if r.status_code != requests.codes.ok:
        print("Error - Exiting" + str(r.status_code))
        exit()

    print(data)
    return_data = r.content.decode(('UTF-8'))
    print(return_data)
    time.sleep(1)

    r = requests.post('http://localhost:5000/print_data', json=data)
    if r.status_code != requests.codes.ok:
        print("Error - Exiting" + str(r.status_code))
        exit()

    time.sleep(1)

    data['data_id'] = data['data_id'] + 1
    data['value'] = data['value'] + 0.1
