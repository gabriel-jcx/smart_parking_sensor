
import threading
import time
from google.cloud import datastore
import os
from datetime import datetime

# set the env variable through the script
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "structure1-0-724fb1f90839.json"

# instantiate the datastore client
datastore_client = datastore.Client()

entity_user = 'Student-Permit-Database'
entity_mobile = 'Mobile-Users-Database'
entity_name = 'East-Remote'
permission = u'C'
subStructure = 0
code = 1234

#photoPath = 'Test_Image.jpg'

global permissionLevelAuth
global codeAuth
global FREE_ERROR
global CLAIM_ERROR
global RESERVE_ERROR
def lot_statistics(date):
   hour_of_day = []

   m = 8
   print('\nCalculating Parking Lot Statistics\n***************************************\n')
   curr = datetime.now()
   while m <= 20:
      query = datastore_client.query(kind='Log_Entity')
      query.add_filter('Date', '=', date)
      query.add_filter('Hour', '=', m)
      n = 0
      for new_log in query.fetch(): #and query_hour.fetch():
         n += 1

      hour_of_day.append(n)
      m += 1
   finish = datetime.now()
   diff = finish - curr
   print diff
   print hour_of_day
lot_statistics("2018.5.2")
