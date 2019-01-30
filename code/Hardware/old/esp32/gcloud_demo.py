from google.cloud import datastore
import os
import datetime

# set the env variable through the script
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "structure1-0-724fb1f90839.json"

# instantiate the datastore client
datastore_client = datastore.Client()

entity_user = 'Student-Permit-Database'
entity_name = 'East-Remote'
permission = u'C'
subStructure = 0

global permissionLevelAuth
global codeAuth
global FREE_ERROR
global CLAIM_ERROR
global RESERVE_ERROR

# This function is called when a car first enters a parking space and
# takes a space_ID obtained from the Sensor Tower and a code deciphered
# by the Gateway in order to mark a space as "Occipued" in the parking lot databae.
# It will also make sure that the user has permission to park in the given space
# by looking at the permisison level of the space and the permission level that the user
# has attributed with their code. In addition to those two features, this function
# also checks if the users permit is currently active in another space or lot.
def claim_space(space, code):
	print ("Claiming space: %s with ID: %s" % (space, code) )
	CLAIM_ERROR = 0;
	codeAuth = 0
	permissionLevelAuth = 0
	
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
			############## CHECK IF CODE IS ACTIVE #################
			active = user_['Active']
			if active == 1:
				print('{} is already in use.'.format(userID))
			else:
				print('Permit not in use')
				user_['Active'] = 1
				datastore_client.put(user_)
			################################################


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
					space_['Timeframe'] = datetime.datetime.now()
					space_['Day'] = datetime.datetime.today().weekday()
					space_['Hour'] = datetime.datetime.now().hour
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
					space_['Day'] = datetime.datetime.today().weekday()
					space_['Hour'] = datetime.datetime.now().hour
					
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
				space_['Day'] = datetime.datetime.today().weekday()
				space_['Hour'] = datetime.datetime.now().hour
				datastore_client.put(space_)
				print('Target Space {} {} was taken'.format(space_['Sub-Structure'], space_.key.name))
				print('Permit Code {} is valid.'.format(code))
		return permissionLevelAuth
# end claim_space()

# This function is called when a car leaves a parking space and sets all the attributes of
# the space to empty or zero
def free_space(space):
	FREE_ERROR = 0;
	ID = 'Space-{}'.format(space)
	with datastore_client.transaction():
		key = datastore_client.key(entity_name, ID)
		space_ = datastore_client.get(key)

		if not space_:
				print('Space {} does not exist.'.format(ID))
		#		FREE_ERROR = 1


		if not space_['Occupied']:
				print('Target Space {} {} {} was unoccupied: ERR'.format(space_['Structure'], space_['Sub-Structure'], space_.key.name))
		#		FREE_ERROR = 1
		else:
			#####################################
			code = space_['Code']
			userID = 'Permit Code-{}'.format(code)
			with datastore_client.transaction():
				key = datastore_client.key(entity_user, userID)
				user_ = datastore_client.get(key)
				
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
			space_['Timeframe'] = datetime.datetime.now()
			
			datastore_client.put(space_)

			print('Target Space {} {} was freed'.format(space_['Sub-Structure'], space_.key.name))
			log_occupant(ID, timeframe, hour, day)
# end free_space()

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
	
	space_key = datastore_client.key(entity_name, space_ID)
	space_ = datastore_client.get(space_key)
	
	time_now = str(datetime.datetime.now())
	new_key = datastore_client.key('Log_Entity', time_now) # Auto-generate key's unique ID
	
	# Prepares the new entity
	new_log = datastore.Entity(key=new_key)
	new_log['Arrival'] = timeframe
	new_log['Departure'] = space_['Timeframe']
	new_log['Space ID'] = space_ID
	new_log['Lot Name'] = u'East Remote'
	new_log['Floor'] = 0
	new_log['Image'] = "image"
	new_log['Hour'] = hour
	new_log['Day'] = day
	
	# Saves the entity
	datastore_client.put(new_log)
	
	print('Saved {} occupied from {} to {}'.format(new_log['Space ID'], new_log['Arrival'], new_log['Departure']))
# end log_occupant()
