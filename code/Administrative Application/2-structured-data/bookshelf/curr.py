
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
      t = threading.Thread(target=log_count, args=(hour_of_day,m,query,day,))
      threads.append(t)
      t.start()
      m += 1
   for t in threads:
      t.join()
   finish = datetime.now()
   print finish - start
   print hour_of_day
   return hour_of_day
