''' This script downloads the latest values from a sentek soilmoisture probe and pushes them to the opensensemap'''
import requests
from datetime import datetime, timedelta
import pytz

from my_secrets import SECRETS

# sentek - data
api_key = SECRETS['SENTEK_API']
database_name = SECRETS['SENTEK_DATABASE']
path = SECRETS['SENTEK_PATH'] # path of a specific graph. 
pane = 0 # 0 corresponds to bottom pane

# sensemap - data
headers = {'content-type': 'application/json'}
sensemap_url = f"https://api.opensensemap.org/boxes/{SECRETS['SENSEBOX_ID']}/data"

# get values from the last five hours
start = (datetime.now() - timedelta(hours=5)).strftime("%Y%m%d%H%M%S")
end = datetime.now().strftime("%Y%m%d%H%M%S")

#print(start, end)

# check if its summertime: https://stackoverflow.com/questions/2881025/python-daylight-savings-time
def is_dst(dt=None, timezone="UTC"):
    if dt is None:
        dt = datetime.utcnow()
    timezone = pytz.timezone(timezone)
    timezone_aware_date = timezone.localize(dt, is_dst=None)
    return timezone_aware_date.tzinfo._dst.seconds != 0

timeZone = "Europe/Berlin"
dt_now = datetime.now()
dst = is_dst(dt_now, timeZone)

# send get request to sentek
sentek_url = f'https://www.irrimaxlive.com/api/?cmd=getgraphvalues&key={api_key}&path={path}&pane={pane}&from={start}&to={end}'
r_sen = requests.get(sentek_url)
print(f'{r_sen.status_code=}')

# process response
text = r_sen.text
#print(text)
last_line = text.split('\r\n')[-2] # last line is empty -> take second last
#print(current_values)

# convert time to RFC3339
time = datetime.strptime(last_line.split(',')[0], '%Y/%m/%d %H:%M:%S')
#print(time)
dst = is_dst(time, timeZone)
#print(dst)

if dst:
        time = time - timedelta(hours=2)
else:
        time = time - timedelta(hours=1)
time_rfc = time.strftime('%Y-%m-%dT%H:%M:%SZ')
#print(time_rfc)

measurements = last_line.split(',')[1:] # remove time to get only measurements
#print(time, measurements)

# send measurements to sensebox
data = {
        f"{SECRETS['measurement_10_id']}" : [measurements[0],time_rfc],
        f"{SECRETS['measurement_20_id']}" : [measurements[1],time_rfc],
        f"{SECRETS['measurement_30_id']}" : [measurements[2],time_rfc],
        f"{SECRETS['measurement_40_id']}" : [measurements[3],time_rfc],
        f"{SECRETS['measurement_60_id']}" : [measurements[4],time_rfc],
        f"{SECRETS['measurement_80_id']}" : [measurements[5],time_rfc],
        f"{SECRETS['measurement_100_id']}": [measurements[6],time_rfc],
}
#print(data)
r_osm = requests.post(sensemap_url, json=data, headers=headers)
print(f'{r_osm.status_code=}')