from databroker import Broker
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

db = Broker.named('chx')
hdr = db[-10]

list_time = []
list_scan_id = []
list_num_imgs = []

hdrs = iter(db())

for hdr in hdrs:
    start_document = hdr.start
    if hdr.db(plan_name='count'):
        if 'time' in start_document:
            list_time.append(start_document['time'])
        if 'scan_id' in start_document:             
        	list_scan_id.append(start_document['scan_id'])
        if 'number of images' in start_document:
            list_num_imgs.append(float(start_document['number of images']))
        else:
            list_num_imgs.append(-1)

chx_info = {'Time' : list_time, 'Scan ID' : list_scan_id, 'Number of Images' : list_num_imgs}

df = pd.DataFrame(chx_info, columns = ['Time', 'Scan ID', 'Number of Images'])

arr = np.array(df['Number of Images'])
arr = arr.astype(float)
arr[~np.isnan(arr)]

plt.ion()

plt.figure()
plt.plot(arr)
