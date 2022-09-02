''' This script downloads the latest values from a sentek soilmoisture probe and pushes them to the opensensemap'''
import requests
import json

#from sentek_api import get_last_values
from secrets import SECRETS

# sentek
SENTEK_API_KEY = SECRETS['SENTEK']
database_name = 'arensnest_sommer'

# sensemap
headers = {'content-type': 'application/json'}
url = f"https://api.opensensemap.org/boxes/{SECRETS['SENSEBOX_ID']}/data"


if __name__ == '__main__':

    # get last values from sentek
    # current_values = get_last_values(key = SENTEK_API_KEY, database = database_name)

    # process the data if needed?

    # send values to sensebox
    data = {
            f"{SECRETS['test_measurement_id']}": "1",
    }

    r = requests.post(url, json=data, headers=headers)

    print(r.status_code)



