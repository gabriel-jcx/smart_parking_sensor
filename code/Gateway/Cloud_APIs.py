from google.cloud import datastore
import os
from datetime import datetime
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


def MAC_map_to_spot(MAC):
   #formatPass = '{}'.format(password)
   with datastore_client.transaction():
      spot_key = datastore_client.key("Sensor_map", MAC)
      spot = datastore_client.get(spot_key)
      if spot:
         parking_lot = spot['Lot Name']
         spot_id = spot['spot_id']
         return parking_lot +":"+str(spot_id)
      else:
         return "MAC cannot be Mapped"  
# Used by the admin to create a new lot with size space_sount
# this function also sets all the parameters of each space within
# the parking lot to empty or zero
def create_lot(space_count):
   i = 0
   while i < space_count:
      i += 1
      ID = 'Space-{}'.format(i)
      new_key = datastore_client.key(parking_lot, ID)
      new_spot = datastore.Entity(key=new_key)
      new_spot['Sub-Structure'] = subStructure
      new_spot['Code'] = 0
      new_spot['License Plate'] = u'Empty'
      new_spot['Permission'] = permission
      new_spot['Occupied'] = False
      new_spot['Authorized'] = False
      new_spot['Request Pic'] = False
      new_spot['Timeframe'] = datetime.now();
      new_spot['Image'] = 'image'
      new_spot['Day'] = 0
      new_spot['Hour'] = 0

      # Saves the entity
      datastore_client.put(new_spot)
      print('Saved {} {} {}: {}'.format(new_spot['Sub-Structure'], new_spot['Code'], new_spot.key.name, new_spot['Occupied']))
# end create_lot()

# This function originally created an "empty" student database
# could have been used by the admin, but doesn't serve much
# functionality due to it only setting all the fields for
# each student to empty or 0
def init_student_database(students):
   i = 0
   j = 1234
   while i < students:
      i += 1
      ID = 'Permit Code-{}'.format(j)
      j += 1
      new_key = datastore_client.key('Student-Permit-Database', ID)
      new_student = datastore.Entity(key = new_key)
      new_student['Name'] = u'Empty'
      new_student['Student ID'] = 0
      new_student['Password'] = u'Empty'
      new_student['Permission Level'] = u'R'
      new_student['License Plate(s)'] = u'Empty'
      datastore_client.put(new_student)
      print('Saved {} {} {} {}: {}'.format(new_student['Name'], new_student.key.name, new_student['Student ID'], new_student['Permission Level'], new_student['License Plate(s)']))
# end init_student_database()
# I used this function only to add the code field to the student database
# This fucntion would not be executed in normal use
def init_mobile_users():
   ID = '7654321'
   new_key = datastore_client.key('Mobile-Users-Database', ID)
   new_student = datastore.Entity(key = new_key)
   new_student['First Name'] = u'Richard'
   new_student['Last Name'] = u'Nixon'
   new_student['Password'] = u'RNixon1'
   new_student['Permit Code'] = u'5784'
   new_student['Permission Level'] = u'R'
   datastore_client.put(new_student)
# end init_mobile_users()
# I created this fucntion for the mobile app to use, so that when they are logging in for the first time
# the user will have to enter their student ID and password in order to receive their permit code to
# use for spot authentication
def auth_mobile_user(studentID, password):
   ID = '{}'.format(studentID)
   #formatPass = '{}'.format(password)
   with datastore_client.transaction():
      new_key = datastore_client.key('Mobile-Users-Database', ID)
      mobile_user = datastore_client.get(new_key)
      if password == mobile_user['Password']:
         print('Password match.')
         print('{} {}s permit code is {}.'.format(mobile_user['First Name'], mobile_user['Last Name'], mobile_user['Permit Code']))
      else:
         print('Incorrect password.')
#end auth_mobile_user()


# I used this function to add student fileds one by one to have
# actuve users in the database to simulate parking
def edit_student():
   j = 1235
   ID = 'Permit Code-{}'.format(j)
   new_key = datastore_client.key('Student-Permit-Database', ID)
   new_student = datastore.Entity(key = new_key)
   new_student['First Name'] = u'Cosmo'
   new_student['Last Name'] = u'Kramer'
   new_student['Student ID'] = u'3456789'
   new_student['Password'] = u'CKramer1'
   new_student['Permission Level'] = u'R'
   new_student['License Plate(s)'] = u'Empty'

   datastore_client.put(new_student)
# end edit_student()


# When a student buys a permit, this fucntion could be used by the administrator to add the student to
# the Student User Database and the Mobile User Database at the same time
def add_student(code, fName, laName, licPlate, password, permLvl, studentID):
   mobileID = '{}'.format(studentID)
   userID = 'Permit Code-{}'.format(code)

   new_key = datastore_client.key('Student-Permit-Database', userID)
   new_student = datastore.Entity(key = new_key)

   new_student['Active'] = 0
   new_student['First Name'] = fName
   new_student['Last Name'] = laName
   new_student['Student ID'] = studentID
   new_student['Password'] = password
   new_student['Permission Level'] = permLvl
   new_student['License Plate(s)'] = licPlate
   datastore_client.put(new_student)

   new_mobile_key = datastore_client.key('Mobile-Users-Database', mobileID)
   new_mobile_user = datastore.Entity(key = new_mobile_key)

   new_mobile_user['First Name'] = fName
   new_mobile_user['Last Name'] = laName
   new_mobile_user['Password'] = password
   new_mobile_user['Permit Code'] = code
   new_mobile_user['Permission Level'] = permLvl
   datastore_client.put(new_mobile_user)
#end add_student()


# I used this function only to add the code field to the student database
# This fucntion would not be executed in normal use
def add_student_field(code):
   ID = 'Permit Code-{}'.format(code)
   with datastore_client.transaction():
      key = datastore_client.key('Student-Permit-Database', ID)
      user = datastore_client.get(key)
      if not user:
         print('{} does not exist.'.format(ID))
      else:
         user['Active'] = 0
         datastore_client.put(user)
# end add_student_field()


# I used this function only to add the request pic field to the student database
# This fucntion would not be executed in normal use
def add_spot_field(space_count):
   i = 0
   while i < space_count:
      i += 1

      ID = 'Space-{}'.format(i)
      with datastore_client.transaction():
         key = datastore_client.key(parking_lot, ID)
         space_ = datastore_client.get(key)
         space_['Request Pic'] = 0
         datastore_client.put(space_)
#end add_spot_field()


# This function was designed to be used by the Aministrator to temporarily change the permission
# of a space of their choosing
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
         space_['Permission'] = new_permission
         datastore_client.put(space_)
         print('{} now has permission level {}.'.format(ID, space_['Permission']))
# end reserve_space()


# This function is designed to be used by the Admininstrator to take a space number and it will return
# the name, license place,
def read_space(space): #for admin to get the attributes of a parking space
   ID = 'Space-{}'.format(space)
   with datastore_client.transaction():
      key = datastore_client.key(parking_lot, ID)
      space_ = datastore_client.get(key)

      authorized = space_['Authorized']
      code = space_['Code']
      licPlate = space_['License Plate']
      occupied = space_['Occupied']
      permission = space_['Permission']
      timeframe = space_['Timeframe']

      ############### GET STUDENT INFORMATION BASED ON CODE IN SAPCE ###############
      userID = 'Permit Code-{}'.format(code)
      with datastore_client.transaction():
         key = datastore_client.key('Student-Permit-Database', userID)
         user_ = datastore_client.get(key)

         fname = user_['First Name']
         lname = user_['Last Name']
         student_perm = user_['Permission Level']
         student_ID = user_['Student ID']

   print('Space: {}, {}, {}, {}, {}, {}, {}'.format(space, occupied, fname, lname, student_perm, code, student_ID))

   if occupied:
      return(1)
   else:
      return(0)
# end read_space()


# This function is used by the administrator in order to reset the defaults of a given
# "space" if the space was previously reserved to some different permission level
def reset_space_defaults(space):
   RESERVE_ERROR = 0
   ID = 'Space-{}'.format(space)
   with datastore_client.transaction():
      key = datastore_client.key(parking_lot, ID)
      space_ = datastore_client.get(key)

      if not space_:
         RESERVE_ERROR = 1
         print('Space {} does not exist.'.format(ID))

      else:
         space_['Permission'] = permission
         datastore_client.put(space_)
         print('{} now has permission level {}.'.format(ID, space_['Permission']))
# end reset_space_defaults()


# This function is used to get the number of students currently parked in any lot under their permit
# the information will be displayed on the home page of our admin web app
def active_users():
   query = datastore_client.query(kind='Student-Permit-Database')
   query.add_filter('Active', '=', 1)
   n = 0
   print('\nRunning Query of Active Users\n*************************************************\n')
   for users in query.fetch():
      n += 1
   print('There are {} active permit users parked'.format(n))
   return n
# end active_users()


# This function can be used by either the Administrator or the Mobile app to show them
# the percentage of the parking lot that is full before they actually click on the
# lot to view it
def query_free_spaces(lot_name):
   query = datastore_client.query(kind=lot_name)
   query.add_filter('Occupied', '=', False)
   n = 0
   print('\nRunning Query of Free Spaces\n*************************************************\n')
   for space_ in query.fetch():
      n+=1

   print('\nThe parking lot is {}% full. \n'.format(n))
# end query_free_spaces()


# This function returns the number spaces in a given parking lot
def query_spaces(parking_lot):
   query = datastore_client.query(kind=parking_lot)
   n = 0
   print('\nRunning Query of Free Spaces\n*************************************************\n')
   for space_ in query.fetch():
      n += 1
   #print('\nThe parking lot is {}% full. \n'.format(n))
   print n
   return n
# end query_free_spaces()


# This function returns the number of free spaces in a given parking lot
# It is called by lot_full_percentage
def query_taken_spaces(parking_lot):
   query = datastore_client.query(kind=parking_lot)
   query.add_filter('Occupied', '=', True)
   space_states = []
   n = 0
   print('\nRunning Query of Free Spaces\n*************************************************\n')
   for space_ in query.fetch():
      n += 1

   return n
# end query_taken_spaces()


# This function returns the percentage that a given lot is full, in addition to the taken spaces
def lot_full_percentage(parking_lot):
   free = query_spaces(parking_lot);
   taken_count = query_taken_spaces(parking_lot);

   quotient = (float)((float)(taken_count) / (float)(free))
   percentage = quotient * 100

   return percentage, taken_count
# end lot_full_percentage()


# This function returns the number of unauthorized cars parked in a given parking lot
def unauthorized_parking(parking_lot):
   print('\nCalculating Number of Illegally Parked Cars\n***************************************\n')
   query = datastore_client.query(kind=parking_lot)
   query.add_filter('Occupied', '=', True)
   query.add_filter('Authorized', '=', False)
   n = 0
   for unauth_spots in query.fetch(): #and query_hour.fetch():
      n += 1

   return n
# end unauthorized_parking


# This fucntion will be used by the Administrator to see how many people were parked in the parking lot
# of their choosing on a given day throughout the quarter or year
def lot_state(parking_lot):
   space_states = []
   free = query_spaces(parking_lot)
   i = 1
   while i <= free:
      ID = 'Space-{}'.format(i)
      i += 1
      #with datastore_client.transaction():
      key = datastore_client.key(parking_lot, ID)
      space = datastore_client.get(key)
      if space['Occupied'] == True:
         n = 1
         space_states.append(n)
      else:
         n = 0
         space_states.append(n)

   print space_states
# end lot_state()


# This function is called by free_space() so when a car leaves the parking lot
# this fucntion will take the space_ID, exact time when the user arrived
# hour of the day the user arrived, and day that the user parked in the
# parking lot and store that information in the Log_Entity
# database for later use in calculating parking statistics
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

   print time_now
   #new_key = datastore_client.key(time_now) # Auto-generate key's unique ID

   # Prepares the new entity
   new_log = datastore.Entity(key=new_key)
   new_log['Arrival'] = timeframe
   new_log['Departure'] = curr_time
   new_log['Space ID'] = space_ID
   new_log['Lot Name'] = u'East Remote'
   new_log['Floor'] = 0
   new_log['Hour'] = hour
   new_log['Day'] = day
   new_log['Date'] = date

   # Saves the entity
   datastore_client.put(new_log)

   print('Saved {} occupied from {} to {}, on {}'.format(new_log['Space ID'], new_log['Arrival'], new_log['Departure'], new_log['Date']))
# end log_occupant()


# This function is executed by the mobile app in order to authenticate in the event
# that the Gateway did not recognize the code that was deciphered or an error occurred
# in the the process of obtaining the users permit code
def mobile_claim(space, code):
   ID = 'Space-{}'.format(space)
   with datastore_client.transaction():
      key = datastore_client.key(parking_lot, ID)
      space_ = datastore_client.get(key)

      if space_['Occupied'] == True:
         if space_['Code'] == 0:
            space_['Code'] = code;
            #print('Space is occupied and code was 0.')
            datastore_client.put(space_)

      else:
         print('Space {} is already authenticated'.format(space))
# end mobile_claim()


# This function is called when a car first enters a parking space and
# takes a space_ID obtained from the Sensor Tower and a code deciphered
# by the Gateway in order to mark a space as "Occipued" in the parking lot databae.
# It will also make sure that the user has permission to park in the given space
# by looking at the permisison level of the space and the permission level that the user
# has attributed with their code. In addition to those two features, this function
# also checks if the users permit is currently active in another space or lot.
def claim_space(space, code):
   CLAIM_ERROR = 0;
   codeAuth = 0
   permissionLevelAuth = 0

   ID = 'Space-{}'.format(space)
   with datastore_client.transaction():
      key = datastore_client.key(parking_lot, ID)
      space_ = datastore_client.get(key)

########check to see if permit code exists in Student Permit Database (SPD)
   userID = 'Permit Code-{}'.format(code)
   with datastore_client.transaction():
      key = datastore_client.key('Student-Permit-Database', userID)
      user_ = datastore_client.get(key)

      if not user_:
         print('Permit code {} does not exist.'.format(userID))
         codeAuth = 0
      else:
         codeAuth = 1
         print('Permit code {} exists.'.format(userID))
         #####################################
         active = user_['Active']
         if active == 1:
            print('{} is already in use.'.format(userID))
         else:
            print('Permit not in use')
            user_['Active'] = 1
            datastore_client.put(user_)
               #############################

      if codeAuth == 1:
         if user_['Permission Level'] <= space_['Permission']:
            print('User has permission to park here')
            permissionLevelAuth = 1

         else:
            print('User DOES NOT have permission to park here')
            permissionLevelAuth = 0

# if the code is in the SPD you can then access the properties (name, student ID,
# License plate num, and permission level thru the variable "user_"
#####################################################################

      if not space_:
         CLAIM_ERROR = 1
         print('Space {} does not exist.'.format(ID))

      else:
         if codeAuth > 0:
            if permissionLevelAuth > 0:
               space_['Code'] = code
               #
               #space_['Image'] = data
               #
               space_['Occupied'] = True
               space_['Authorized'] = True
               space_['Timeframe'] = datetime.now()
               space_['Day'] = datetime.today().weekday()
               space_['Hour'] = datetime.now().hour

               datastore_client.put(space_)
               print('Target Space {} {} was taken'.format(space_['Sub-Structure'], space_.key.name))
            else:
               space_['Code'] = code
               #
               #space_['Image'] = data
               #
               space_['Occupied'] = True
               space_['Authorized'] = False
               space_['Timeframe'] = datetime.now()
               space_['Day'] = datetime.today().weekday()
               space_['Hour'] = datetime.now().hour
               datastore_client.put(space_)
               print('Target Space {} {} was taken'.format(space_['Sub-Structure'], space_.key.name))

         else:
            CLAIM_ERROR = 1
            space_['Code'] = 0
            #
            #space_['Image'] = data
            #
            space_['Occupied'] = True
            space_['Authorized'] = False
            space_['Timeframe'] = datetime.now()
            space_['Day'] = datetime.today().weekday()
            space_['Hour'] = datetime.now().hour
            datastore_client.put(space_)
            print('Target Space {} {} was taken'.format(space_['Sub-Structure'], space_.key.name))
            print('Permit Code {} is invalid.'.format(code))


   return (CLAIM_ERROR)
   #if not space_['Occupied']:
     # print('ERROR: The target space was not occuppied.')
    #  CLAIM_ERROR = 1
      #return(CLAIM_ERROR)
   #else:
      #return(0)
# end claim_space()


# This function is called when a car leaves a parking space and sets all the attributes of
# the space to empty or zero
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
         code = space_['Code']
         # added code existence checking
         if not code:
            print "NO authorized user at this spot"
            FREE_ERROR = 1
            return FREE_ERROR 
         userID = 'Permit Code-{}'.format(code)
         with datastore_client.transaction():
            key = datastore_client.key('Student-Permit-Database', userID)
            user_ = datastore_client.get(key)
            user_['Active'] = 0
            datastore_client.put(user_)
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

def parking_test():
   claim_space(1, 1241)
   claim_space(2, 1239)
   claim_space(3, 1240)
   claim_space(4, 1245)
   claim_space(5, 1244)
#	claim_space(15, 1234)
#	claim_space(16, 1234)
#	claim_space(17, 1234)
#	claim_space(18, 1234)
#	claim_space(19, 1234)
#query_free_spaces()
#query_log_entities()

def free_test():
   free_space(1)
   free_space(2)
   free_space(3)
   free_space(4)
   free_space(5)
#free_space(15)
#free_space(16)
#free_space(17)
#free_space(18)
#free_space(19)

