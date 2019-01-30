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

#photoPath = 'Test_Image.jpg'

global permissionLevelAuth
global codeAuth
global FREE_ERROR
global CLAIM_ERROR
global RESERVE_ERROR
def link_ble(parking_lot, spot_id, MAC):
   sensor_key = datastore_client.key("Sensor_map",unicode(MAC))
   new_sensor = datastore.Entity(key=sensor_key)
   new_sensor['Lot Name'] = unicode(parking_lot)
   new_sensor['MAC'] = unicode(MAC)
   new_sensor['spot_id'] = spot_id
   datastore_client.put(new_sensor)

# When a student buys a permit, this fucntion could be used by the administrator to add the student to
# the Student User Database and the Mobile User Database at the same time
def add_student(code, fName, laName, licPlate, password, permLvl, studentID, expire_days):
   mobileID = '{}'.format(studentID)
   userID = 'Permit Code-{}'.format(code)

   new_key = datastore_client.key('Student-Permit-Database', userID)
   new_student = datastore.Entity(key = new_key)

   new_student['Active'] = 0
   new_student['Permit Code'] = unicode(code)
   new_student['First Name'] = unicode(fName)
   new_student['Last Name'] = unicode(laName)
   new_student['Student ID'] = unicode(studentID)
   new_student['Password'] = unicode(password)
   new_student['Permission Level'] = unicode(permLvl)
   new_student['License Plate(s)'] = unicode(licPlate)
   new_student['Expiration'] = datetime.now() + timedelta(days=expire_days)
   datastore_client.put(new_student)

   new_mobile_key = datastore_client.key('Mobile-Users-Database', mobileID)
   new_mobile_user = datastore.Entity(key = new_mobile_key)

   new_mobile_user['First Name'] = unicode(fName)
   new_mobile_user['Last Name'] = unicode(laName)
   new_mobile_user['Password'] = unicode(password)
   new_mobile_user['Permit Code'] = unicode(code)
   new_mobile_user['Permission Level'] = unicode(permLvl)
   new_mobile_user['Expiration'] = datetime.now() + timedelta(days=expire_days)
   datastore_client.put(new_mobile_user)
#end add_student()

def claim_space(space, code):
    CLAIM_ERROR = 0;
    codeAuth = 0
    permissionLevelAuth = 0
    reserved = 0
    curr = datetime.now()
    day = unicode(datetime.today().weekday())
    hour = unicode(curr.hour)
    time = unicode(curr)
    
    ID = 'Space-{}'.format(space)
    with datastore_client.transaction():
        key = datastore_client.key(parking_lot, ID)
        space = datastore_client.get(key)

        if not space: # space does not exist
            CLAIM_ERROR = 1
            print('Space {} does not exist.'.format(ID))

        else: # space exists
        
########check to see if permit code exists in Student Permit Database (SPD)
# if the code is in the SPD you can then access the properties (name, student ID,
# License plate num, and permission level thru the variable "user"
#####################################################################
            userID = 'Permit Code-{}'.format(code)
            with datastore_client.transaction():
                key = datastore_client.key('Student-Permit-Database', userID)
                user = datastore_client.get(key)

                if not user: # code does not exist
                    print('Permit code {} does not exist.'.format(userID))
                    codeAuth = 0
            
                # student permit has passed its expiration date
                elif str(datetime.now()) > str(user['Expiration']):
                    print('User Permit has expired')
                    codeAuth = 0
            
                elif space['Permission'] == 'Reserved': # space is marked as reserved
                    reserved = 1
                    print ('Space is reserved for Guest Parking')
                    if user['Permission Level'] == 'Reserved':
                        codeAuth = 1 # student is a guest with permission level of Reserved
                        permissionLevelAuth = 1
                    else: # student permit is valid, but is NOT permission level Reserved
                        codeAuth = 1
                        permissionLevelAuth = 0
                
                else: # code was found in SPD
                    codeAuth = 1
                    print('Permit code {} exists.'.format(userID))
                    active = user['Active']
                    if active == 1:
                        print('{} is already in use.'.format(userID))
                    else:
                        print('Permit not in use')
                        user['Active'] = 1
                        datastore_client.put(user)
                ####### check if user has permission to park here ##########
                        if user['Permission Level'] <= space['Permission']:
                            print('User has permission to park here')
                            permissionLevelAuth = 1
                        else:
                            print('User DOES NOT have permission to park here')
                            permissionLevelAuth = 0

#####################################################################
# space exists and can now be marked as occupied in the database    #
#####################################################################
                space['Occupied'] = True
                space['Timeframe'] = time
                space['Day'] = day
                space['Hour'] = hour
                if codeAuth > 0: # permit has permission to park in space
                    if permissionLevelAuth > 0:
                        space['Code'] = code
                        space['Authorized'] = True
                        datastore_client.put(space)
                        print('Target Space {} was taken'.format(space.key.name))
                    else: # permit does not have permission to park in space
                        CLAIM_ERROR = 1
                        space['Code'] = code
                        space['Authorized'] = False
                        datastore_client.put(space)
                        print('Target Space {} was taken'.format(space.key.name))
                else: # code was not detected or an error occurred while deciphering
                    CLAIM_ERROR = 2
                    space['Code'] = 0
                    space['Authorized'] = False
                
                    datastore_client.put(space)
                    print('Target Space {} was taken'.format(space.key.name))

    return CLAIM_ERROR
# end claim_space()

def free_space(space):
    FREE_ERROR = 0;
    ID = 'Space-{}'.format(space)
    with datastore_client.transaction():
        key = datastore_client.key(parking_lot, ID)
        space_ = datastore_client.get(key)

        if not space_:
                print('Space {} does not exist.'.format(ID))
                FREE_ERROR = 1

        else:
            #####################################
            code = space_['Code']
            userID = 'Permit Code-{}'.format(code)
            with datastore_client.transaction():
            
                key = datastore_client.key('Student-Permit-Database', userID)
                user_ = datastore_client.get(key)
                if user_:
                    user_['Active'] = 0
                    datastore_client.put(user_)
            ##################################
            
            space_['Code'] = 0
            space_['Occupied'] = False
            space_['Authorized'] = False
            timeframe = space_['Timeframe']
            day = space_['Day']
            hour = space_['Hour']
            space_['Day'] = 0
            space_['Hour'] = 0
            space_['Timeframe'] = datetime.now()
            datastore_client.put(space_)

            print('Target Space {} {} was freed'.format(space_['Sub-Structure'], space_.key.name))
            log_occupant(ID, timeframe, hour, day)
    if space_['Occupied']:
        print('ERROR: The target space was not freed.')
        FREE_ERROR = 1
        return(FREE_ERROR)
    else:
        return(0)
# end free_space()

def log_occupant(space_ID, timeframe, hour, day):
   # log_occupant() creates a small lot of {space_count} spaces
   # Initializes "Space" Entities with string key 'ID' = SSFA-#
   #
   # NOTE: This function will allocate a lingering Google Datastore Entitiy

   space_key = datastore_client.key(parking_lot, space_ID)
   space_ = datastore_client.get(space_key)

   curr_time = datetime.now()
   time_now = unicode(str(datetime.now()))
   date = unicode(str(curr_time.year)+"."+str(curr_time.month)+"."+str(curr_time.day))
   new_key = datastore_client.key('Log_Entity', time_now) # Auto-generate key's unique ID

   month = unicode(str(curr_time.month))
   year = unicode(str(curr_time.year))
   print (time_now)
   #new_key = datastore_client.key(time_now) # Auto-generate key's unique ID

   # Prepares the new entity
   new_log = datastore.Entity(key=new_key)
   new_log['Arrival'] = timeframe
   new_log['Departure'] = curr_time
   new_log['Space ID'] = space_ID
   new_log['Lot Name'] = unicode(parking_lot)
   new_log['Floor'] = 0
   new_log['Hour'] = hour
   new_log['Day'] = day
   new_log['Month'] = month
   new_log['Year'] = year
   new_log['Date'] = date

   # Saves the entity
   datastore_client.put(new_log)

   print('Saved {} occupied from {} to {}, on {}'.format(new_log['Space ID'], new_log['Arrival'], new_log['Departure'], new_log['Date']))
# end log_occupant()


def add_student_field():
    i = 1234
    while i <= 1255:
        ID = 'Permit Code-{}'.format(i)
        with datastore_client.transaction():
            key = datastore_client.key('Student-Permit-Database', ID)
            user = datastore_client.get(key)
            if not user:
                print('{} does not exist.'.format(ID))
            else:
                user['Expiration'] = datetime.now() + timedelta(days=365)
                datastore_client.put(user)
        i += 1
# end add_student_field()

def reserve_space(space, new_permission):
   RESERVE_ERROR = 0
   ID = 'Space-{}'.format(space)
   with datastore_client.transaction():
      key = datastore_client.key(parking_lot, ID)
      space_ = datastore_client.get(key)

      if not space_:
         RESERVE_ERROR = 1
         print('Space {} does not exist.'.format(ID))

      else:
         space_['Permission'] = unicode(new_permission)
         datastore_client.put(space_)
         print('{} now has permission level {}.'.format(ID, space_['Permission']))
# end reserve_space()

#add_student('4321', 'Anujan', 'Varma', '7TIG948', 'AVarma1', 'Reserved', '1029384', 1)
#add_student(1, 1, 1, 1, 1, 'A', 1, 1)
#claim_space(8, 4321)
link_ble("East-Remote",1,"F8061EA4AE30")

