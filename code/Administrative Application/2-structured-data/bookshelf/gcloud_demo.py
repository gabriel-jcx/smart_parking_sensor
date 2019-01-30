from google.cloud import datastore
import os
import datetime

# set the env variable through the script
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "bookshelf/structure1-0-724fb1f90839.json"

# instantiate the datastore client
datastore_client = datastore.Client()

entity_user = 'Student-Permit-Database'
entity_name = 'East-Remote'
entity_mobile= 'Mobile-Users-Database'
entity_admin = 'Admins-Database'
permission = u'C'
subStructure = 0
code = 1234

#photoPath = 'Test_Image.jpg'

global permissionLevelAuth
global codeAuth
global FREE_ERROR
global CLAIM_ERROR
global RESERVE_ERROR

def create_lot(space_count):
	# init_aray() creates a small lot of {space_count} spaces
	# Initializes "Space" Entities with string key 'ID' = SSFA-#
	#
	# NOTE: I used init_array to initialize the spots. Running init_array again
	# will re-create the same spaces. Clean up datastore drive as needed to remove all
	# spaces if they are not being used.

	i = 0
	while i < space_count:
		i += 1

		ID = 'Space-{}'.format(i)

		new_key = datastore_client.key(entity_name, ID)

		# Prepares the new entity
		new_spot = datastore.Entity(key=new_key)
		new_spot['Sub-Structure'] = subStructure
		new_spot['Code'] = 0
		new_spot['License Plate'] = u'Empty'
		new_spot['Permission'] = permission
		new_spot['Occupied'] = False
		new_spot['Authorized'] = False
		new_spot['Timeframe'] = datetime.datetime.now();
		#new_spot['Image'] = 'image'

		# Saves the entity
		datastore_client.put(new_spot)
		print('Saved {} {} {}: {}'.format(new_spot['Sub-Structure'], new_spot['Code'], new_spot.key.name, new_spot['Occupied']))

# end init_aray()
def auth_mobile_user(studentID, password):
   ID = '{}'.format(studentID)
   #formatPass = '{}'.format(password)
   with datastore_client.transaction():
      new_key = datastore_client.key(entity_mobile, ID)
      mobile_user = datastore_client.get(new_key)
      if not mobile_user:
         return "Invalid"
      if password == mobile_user['Password']:
         print('Password match.')
         print('{} {}s permit code is {}.'.format(mobile_user['First Name'], mobile_user['Last Name'], mobile_user['Permit Code']))
         return "{}".format(mobile_user['Permit Code'])
      else:                                                                 
         print('Incorrect password.')
         return "Invalid"

def add_user(database_name, username, password): 
   print("trying to add")
   new_database(database_name, username, password)

def new_database(database_name,username, password):
   with datastore_client.transaction():
      new_key = datastore_client.key(database_name, username)
      new_user = datastore.Entity(key = new_key)
      new_user['Password'] = password
      datastore_client.put(new_user)
      print("Success")

def get_password(studentID, fName, lName, database_name):
   ID = '{}'.format(studentID)
   with datastore_client.transaction():
      user_key = datastore_client.key(database_name, ID)
      if not user_key:
         return "ERROR"
      user = datastore_client.get(user_key)
      if not user:
         return "ID ERROR"
      if fName == user['First Name'] and lName == user['Last Name']:
         passwd = user['Password']
         return passwd
      else:
         return "Invalid Name"




#This function is a more universal version of the authentication of any user
# The function takes in an additional parameter as the database_name to look
# in the datastore
def auth_user(username, password, database_name):
   ID = '{}'.format(username)
   print ID
   with datastore_client.transaction():
      user_key = datastore_client.key(database_name, ID)
      if not user_key:
         return "Database " + database_name + " doesn't exist"
      user = datastore_client.get(user_key)
      if not user:
         return "Invalid" #This says user doesn't exist in that database
      if password == user['Password']:
         print('Password match.')
         return 'Login success'
      else:
         print('Incorrect password.')
         return "Invalid"


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

def edit_student():
	
	j = 1239
	ID = 'Permit Code-{}'.format(j)
	new_key = datastore_client.key('Student-Permit-Database', ID)
		
	new_student = datastore.Entity(key = new_key)
	new_student['Name'] = u'Winston'
	new_student['Student ID'] = 0
	new_student['Password'] = u'Empty'
	new_student['Permission Level'] = u'R'
	new_student['License Plate(s)'] = u'Empty'
		
	datastore_client.put(new_student)
	print('Saved {} {} {} {}: {}'.format(new_student['Name'], new_student.key.name, new_student['Student ID'], new_student['Permission Level'], new_student['License Plate(s)']))

# end edit_student()

def read_space(space):
	ID = 'Space-{}'.format(space)
	with datastore_client.transaction():
		key = datastore_client.key(entity_name, ID)
		space_ = datastore_client.get(key)

		authorized = space_['Authorized']
		code = space_['Code']
		licPlate = space_['License Plate']
		occupied = space_['Occupied']
		permission = space_['Permission']
		timeframe = space_['Timeframe']

	if occupied:
		return(1)
	else:
		return(0)

# end read_space()

def reset_space_defaults(space):
	RESERVE_ERROR = 0
	ID = 'Space-{}'.format(space)
	with datastore_client.transaction():
		key = datastore_client.key(entity_name, ID)
		space_ = datastore_client.get(key)

		if not space_:
			RESERVE_ERROR = 1
			print('Space {} does not exist.'.format(ID))
		
		else:
			space_['Permission'] = permission
			datastore_client.put(space_)
			print('{} now has permission level {}.'.format(ID, space_['Permission']))

# end reset_space_defaults()

def log_occupant(space_ID, timeframe):
	# log_occupant() creates a small lot of {space_count} spaces
	# Initializes "Space" Entities with string key 'ID' = SSFA-#
	# 
	# NOTE: This function will allocate a lingering Google Datastore Entitiy
	
	space_key = datastore_client.key(entity_name, space_ID)
	space_ = datastore_client.get(space_key)

	new_key = datastore_client.key('Log_Entity') # Auto-generate key's unique ID

	# Prepares the new entity
	new_log = datastore.Entity(key=new_key)
	new_log['Arrival'] = timeframe
	new_log['Departure'] = space_['Timeframe']
	new_log['Space ID'] = space_ID
	new_log['Lot Name'] = u'East Remote'
	new_log['Floor'] = 0
	new_log['Image'] = "image"

	# Saves the entity
	datastore_client.put(new_log)

	print('Saved {} occupied from {} to {}'.format(new_log['Space ID'], new_log['Arrival'], new_log['Departure']))

# end log_occupant()
	
def claim_space(space): # accept IMAGE as well if auth == 0 the permit code is not valid
	#upload_url = blobstore.create_upload_url('Test_Image.jpg')
	code=1234
	CLAIM_ERROR = 0
	codeAuth = 0
	permissionLevelAuth = 0
	
	# pick an image file you have in the working directory
	# or give the full file path ...
	#fin = open(photoPath, "rb")
	#data = fin.read()
	#fin.close()
	
	ID = 'Space-{}'.format(space)
	with datastore_client.transaction():
		key = datastore_client.key(entity_name, ID)
		space_ = datastore_client.get(key)
	
########check to see if permit code exists in Student Permit Database (SPD)
	userID = 'Permit Code-{}'.format(code)
	with datastore_client.transaction():
		key = datastore_client.key(entity_user, userID)
		user_ = datastore_client.get(key)

		if not user_:
			print('Permit code {} does not exist.'.format(userID))
			codeAuth = 0
		else:
			codeAuth = 1
			print('Permit code {} exists.'.format(userID))

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


		#if space_['Occupied']:
			#CLAIM_ERROR = 1
			#print('Target Space {} {} {} was occupied: ERR'.format(space_['Structure'], space_['Sub-Structure'], space_.key.name))
		
		else:
			if codeAuth > 0:
				if permissionLevelAuth > 0:
					space_['Code'] = code
					#
					#space_['Image'] = data
					#
					space_['Occupied'] = True
					space_['Authorized'] = True
					space_['Timeframe'] = datetime.datetime.now()
					datastore_client.put(space_)
					print('Target Space {} {} was taken'.format(space_['Sub-Structure'], space_.key.name))
				else:
					space_['Code'] = code
					#
					#space_['Image'] = data
					#
					space_['Occupied'] = True
					space_['Authorized'] = False
					space_['Timeframe'] = datetime.datetime.now()
					
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
				space_['Timeframe'] = datetime.datetime.now()
				datastore_client.put(space_)
				print('Target Space {} {} was taken'.format(space_['Sub-Structure'], space_.key.name))
				print('Permit Code {} is valid.'.format(code))

# end claim_space()

def free_space(space):
	FREE_ERROR = 0;
	ID = 'Space-{}'.format(space)
	with datastore_client.transaction():
		key = datastore_client.key(entity_name, ID)
		space_ = datastore_client.get(key)

		if not space_:
				print('Space {} does not exist.'.format(ID))
				FREE_ERROR = 1


		#if not space_['Occupied']:
		#		print('Target Space {} {} {} was unoccupied: ERR'.format(space_['Structure'], space_['Sub-Structure'], space_.key.name))
		#		FREE_ERROR = 1
		else:
			space_['Code'] = 0
			space_['Occupied'] = False
			space_['Authorized'] = False
			timeframe = space_['Timeframe']
			space_['Timeframe'] = datetime.datetime.now()
			datastore_client.put(space_)

			print('Target Space {} {} was freed'.format(space_['Sub-Structure'], space_.key.name))
			log_occupant(ID, timeframe)

# end free_space()

def reserve_space(space):
   CLAIM_ERROR = 0;
   codeAuth = 0
   permissionLevelAuth = 0
	
   ID = 'Space-{}'.format(space)
   with datastore_client.transaction():
      key = datastore_client.key(entity_name, ID)
      space_ = datastore_client.get(key)
      if not space_:
         CLAIM_ERROR = 1
         print('Space {} does not exist.'.format(ID))


      #if space_['Occupied']:
      #   CLAIM_ERROR = 1
      #   print('Target Space {} {} {} was occupied: ERR'.format(space_['Structure'], space_['Sub-Structure'], space_.key.name))
		
      else:
         space_['Occupied'] = True
         space_['Authorized'] = True
         space_['Timeframe'] = datetime.datetime.now()
         datastore_client.put(space_)
         print('Target Space {} {} was taken'.format(space_['Sub-Structure'], space_.key.name))
   change_space_permission(space, u'Reserved')
   
#end reserve_space()

def change_space_permission(space, new_permission):
	RESERVE_ERROR = 0
	ID = 'Space-{}'.format(space)
	with datastore_client.transaction():
		key = datastore_client.key(entity_name, ID)
		space_ = datastore_client.get(key)

		if not space_:
			RESERVE_ERROR = 1
			print('Space {} does not exist.'.format(ID))

		else:
			space_['Permission'] = new_permission
			datastore_client.put(space_)
			print('{} now has permission level {}.'.format(ID, space_['Permission']))
	return RESERVE_ERROR
# end change_space_permission()

def change_lot_permission(permission):
   CLAIM_ERROR = 0;
   codeAuth = 0
   permissionLevelAuth = 0
   space = 1
   while True:
      error = change_space_permission(space, permission)
      if error:
         break
      space += 1
# end change_lot_permission()
