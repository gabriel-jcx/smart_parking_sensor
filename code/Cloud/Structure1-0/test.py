import threading
import time
from google.cloud import datastore
import os
from datetime import datetime
from datetime import timedelta

# set the env variable through the script
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "structure1-0-724fb1f90839.json"

# instantiate the datastore client
datastore_client = datastore.Client()

entity_user = 'Student-Permit-Database'
entity_mobile = 'Mobile-Users-Database'
parking_lot = 'East-Remote'
permission = u'C'
subStructure = 0
code = 1234
def day_of_week_count(hour_of_day, m, query, day):
   query.add_filter('Day', '=', day)
   query.add_filter('Hour', '=', m)
   n = 0
   for new_log in query.fetch(): #and query_hour.fetch():
      n += 1
   hour_of_day[m-8] = n
def lot_statistics(day):
   hour_of_day = [None]*13
   threads = []
   m = 8
   start = datetime.now()
   #print('\nCalculating Parking Lot Statistics\n***************************************\n')
   while m <= 20:
      query = datastore_client.query(kind='Log_Entity')
      t = threading.Thread(target=day_of_week_count, args=(hour_of_day,m,query,day,))
      threads.append(t)
      t.start()
      m += 1
   for t in threads:
      t.join()
   finish = datetime.now()
   print finish - start
   print hour_of_day
   return hour_of_day
lot_statistics("2018.6.3")
