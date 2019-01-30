# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.ure1-0-724fb1f90839.json was not found.

# this file was built from the google cloud bookshelf example.
import json
from bookshelf import get_model
from datetime import datetime
from datetime import timedelta
from flask import Blueprint, redirect, render_template, request, url_for,make_response,session,jsonify,Response,Markup
from crypt import crypt
import socket
import time
import threading
import base64
import struct
import numpy as np
from Crypto import Random
from Crypto.Cipher import AES
from binascii import unhexlify
BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
class AESCipher:
   def __init__( self, key ,iv):
      self.key = key
      self.iv = iv
   def encrypt( self, raw ):
      raw = pad(raw)
      #iv = Random.new().read( AES.block_size )
      #print np.uint64(int(iv.encode('hex'),16))
      cipher = AES.new( self.key, AES.MODE_CBC, self.iv )
      #return base64.b64encode( iv + cipher.encrypt( raw ) )
      return cipher.encrypt(raw)
   """
   def decrypt( self, enc ):
      enc = base64.b64decode(enc)
      iv = enc[:16]
      cipher = AES.new(self.key, AES.MODE_CBC, iv )
      return unpad(cipher.decrypt( enc[16:] ))
   """

key1 = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01'
key2 = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02'
key3 = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03'
key4 = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04'
key5 = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05'
def bloom_filter_query(param_iv):
   iv = ''
   query_index = []
   #bloom = [0] *58
   for i in param_iv:
      temp = chr(i)
      iv += (temp)
   cipher1 = AESCipher(key1,iv)
   encrypted1 = cipher1.encrypt('test')
   cipher1_text = ""
   cipher2_text = ""
   cipher3_text = ""
   cipher4_text = ""
   cipher5_text = ""
   for i in range(0,len(encrypted1)):
      cipher1_text = cipher1_text + str(int(encrypted1[i].encode('hex'),16))
   query_index.append(int(cipher1_text)%58)
   cipher2 = AESCipher(key2,iv)
   encrypted2 = cipher2.encrypt('test')
   for i in range(0,len(encrypted2)):
      cipher2_text = cipher2_text + str(int(encrypted2[i].encode('hex'),16))
   query_index.append(int(cipher2_text)%58)
   #print (int(encrypted2.encode('hex'),16))
   cipher3 = AESCipher(key3,iv)
   encrypted3 = cipher3.encrypt('test')
   for i in range(0,len(encrypted3)):
      cipher3_text = cipher3_text + str(int(encrypted3[i].encode('hex'),16))
   query_index.append(int(cipher3_text)%58)
   #print (int(encrypted3.encode('hex'),16))
   cipher4 = AESCipher(key4,iv)
   encrypted4 = cipher4.encrypt('test')
   for i in range(0,len(encrypted4)):
      cipher4_text = cipher4_text + str(int(encrypted4[i].encode('hex'),16))
   query_index.append(int(cipher4_text)%58)
   #print (int(encrypted4.encode('hex'),16))
   cipher5 = AESCipher(key5,iv)
   encrypted5 = cipher5.encrypt('test')
   for i in range(0,len(encrypted5)):
      cipher5_text = cipher5_text + str(int(encrypted5[i].encode('hex'),16))
   query_index.append(int(cipher5_text)%58)
   return query_index

# database names to refer to when we need to change parameters of a parking spot
eastRemote = "East-Remote"
westRemote = "West-Remote"
northRemote = "North-Remote"
coreWestRemote = "Core-West"


start = datetime.now()
month_stats_east=[0]*13
month_stats_west=[0]*13
month_stats_north=[0]*13
prev_month = str(start.month)


# routing that determines the set of urls that this file handles. This one handles routes with no prefix i.e. .com/asdf
crud = Blueprint('crud', __name__)

# The following route deal with bloom filter query for the secret symmetric key between the mobile app and the web app
@crud.route("bloom_filter",methods=['GET','POST'])
def bloom_query():
   if request.method == "POST":
      js = json.loads(request.data)
      print(js)
      bloom = js['bloom']
      print(bloom)
      iv = js['iv']
      print(iv)
      bloom_filter = bloom_filter_query(iv)
      print bloom_filter
      for i in bloom_filter:
         if not(bloom[i] == 1):
            print "Error not from mobile app"
            return "fail"
      print "Authenticaed from mobile app"
      return "success"

@crud.route("usr/map_ble",methods=['GET','POST'])
def ble_mapping():
   if request.method == "POST":
      js = json.loads(request.data)
      print(js)
      # gets the username oldpassword and newpassword
      spot_array = []
      for device in js:
         MAC = device['URL']
         print(MAC)
         lot_spot = MAC_map_to_spot(MAC)
         print "The return spot id is: " + lot_spot
         if(lot_spot != "MAC cannot be Mapped"):
            spot_array.append(lot_spot)
      print spot_array
      resp = {}
      resp['spots'] = spot_array
      #resp[corewest_percentage'] = corewest_
      return json.dumps(resp)

      #oldpasswd = js['oldpassword']

@crud.route("Register/ble",methods=['GET','POST'])
def link_ble_to_spot():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   if request.method == 'POST':
      parking_lot = request.form['parking_lot']
      spot_id = request.form['spot_id']
      MAC = request.form['MAC']
      link_ble(parking_lot,spot_id,MAC)
   return render_template("link_ble.html")
# a depricated page for template table
@crud.route("form")
def display_form():
   # a hard coded example for table in view image
   space, authorized, student_ID, fName, lName, licPlate, student_perm, code=read_space(eastRemote,2)
   print space, authorized, student_ID, fName, lName, licPlate, student_perm, code
   space = eastRemote+"        "+ str(space)
   return render_template("table.html",space=space, authorized=authorized,student_ID=student_ID,fName=fName,lName=lName,licPlate=licPlate,student_perm=student_perm,code=code)


@crud.route("dashboard")
def temp_menu():
   # menu url routing
   # a basic check for cookies that all functions have to make sure admin doesnt have to relog for every page.
   # also use for authentication
   # probably would make the cookie checking log better instead of "if not"
   username = request.cookies.get('username')
   if not username:
      # if cookie data is invalid redirect to the login page
      return redirect("/")
   curr = datetime.now()
   date = str(curr.year) + "." + str(curr.month) + "." + str(curr.day)
   print date
   # month array to display month in text
   months = ['January','February','March','April','May','June','July',
         'August','September','Octorber','November','December']

   # get the traffic count of all lots today
   traffic = lot_statistics_today(date)
   print "Traffic is: "
   print traffic

   active_user_count = active_users()

   # illegal parking counts in different lots
   illegal_north = unauthorized_count(northRemote)
   illegal_west = unauthorized_count(westRemote)
   illegal_east = unauthorized_count(eastRemote)
   # lot percentage
   west_percentage = lot_full_percentage(westRemote)
   east_percentage = lot_full_percentage(eastRemote)
   north_percentage = lot_full_percentage(northRemote)
   # number of taken spots
   west_taken = query_taken_spaces(westRemote)
   east_taken = query_taken_spaces(eastRemote)
   north_taken = query_taken_spaces(northRemote)
   month = months[int(curr.month)-1]+ "  "+ str(curr.year)
   end = datetime.now()
   time_elapsed = end - curr
   print ("Time to render dashboard is : {}".format(time_elapsed))
   return render_template("dashboard.html", traffic=traffic, month=month,active_users=active_user_count,il_north=illegal_north,il_west=illegal_west,il_east=illegal_east, west_percentage=west_percentage, east_percentage=east_percentage,north_percentage=north_percentage,west_taken=west_taken,east_taken=east_taken,north_taken=north_taken)

# This url is for mobile app the access the data in google cloud for the percentage taken in a specific lot
@crud.route("usr/query_stats",methods=['GET','POST'])
def query_stats():
   # if a post request happens, return json objects (used by mobile app)
   if request.method == 'POST':
      js = json.loads(request.data)
      print(js)
      bloom = js['bloom']
      iv = js['iv']
      bloom_filter = bloom_filter_query(iv)
      print bloom_filter
      for i in bloom_filter:
         if (bloom[i] == 0):
            print "Error not from mobile app"
            return "fail"
      print "Authenticaed from mobile app"
      west_percentage = lot_full_percentage(westRemote)
      east_percentage = lot_full_percentage(eastRemote)
      #Two lines comment out since no north or core west yet
      north_percentage = lot_full_percentage(northRemote)
      #corewest_percentage = lot_full_percentage(coreWestRemote)
      resp = {}
      resp['west_percentage'] = int(west_percentage)
      resp['east_percentage'] = int(east_percentage)
      resp['north_percentage'] = int(north_percentage)
      #resp[corewest_percentage'] = corewest_
      return json.dumps(resp)


# was gonna implement public key cryptography itself on the web app until i realize the web app can be accessed via https
@crud.route("public_key",methods=['GET','POST'])
def give_publick_key():
   # give public key to requesters
   f = open("bookshelf/static/keys/public.key","r")
   public_key = f.read()
   f.close()
   print public_key
   return public_key

# a tcp test for connecting to gateway, depricated
@crud.route("test_tcp")
def test_tcp():
   # simple tcp socket protocol
   print "established???"
   s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   result = s.connect_ex(("169.233.172.217",6002))
   print result
   print "established???"
   s.send("random shit")
   return render_template("index.html")

# url for user to change password on the mobile app
@crud.route("authenticate/changepasswd", methods=['GET','POST'])
def changepasswd():
   # allows the mobile users to change their pass
   if request.method == 'POST':
      js = json.loads(request.data)
      # gets the username oldpassword and newpassword
      username = js['username']
      oldpasswd = js['oldpassword']
      newpasswd = js['newpassword']
      print username
      print oldpasswd
      print newpasswd
      #change in the database
      result = change_passwd(username,oldpasswd,newpasswd)
      print result
      resp = {}
      resp['stat'] = result
      return json.dumps(resp)
#[START CHART]
@crud.route("stats", methods=['GET','POST'])
def draw():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   # if a post request happens, extract the date that was picked from the calendar
   if request.method == 'POST':
      oldDate = request.form['datepicker']
      # oldDate var is in format month/day/year need to convert to format below
      
      # year.month.day
      if (int(oldDate[0])  == 0):
         reformMonth = oldDate[1:2]
      else:
         reformMonth = oldDate[0:2]
      if (int(oldDate[3])  == 0):
         reformDay = oldDate[4:5]
      else:
         reformDay = oldDate[3:5]
         
      reformYear = oldDate[6:len(oldDate)]
      newDate = reformYear + "." + reformMonth + "." + reformDay
      pickedDate = lot_statistics_today(newDate)
      # set flag to tell page that a date has been picked and to display something different
      flag = 1
      return render_template("chart.html", monday=pickedDate, flag=flag, showDate=newDate)
   # if no post request then default to displaying weekly stats    
   monday=lot_statistics(0)
   tuesday=lot_statistics(1)
   wednesday=lot_statistics(2)
   thursday=lot_statistics(3)
   friday=lot_statistics(4)
   saturday=lot_statistics(5)
   sunday=lot_statistics(6)
   flag = 0
   return render_template("chart.html", sunday=sunday, monday=monday, tuesday=tuesday, wednesday=wednesday, thursday=thursday, friday=friday, saturday=saturday, flag=flag)
#[END CHART]

# This url is used to handle the post request that
# came from the Mobile app that takes in the username
# and the password, then look into the google cloud
# finally returns the Permit Code
@crud.route("authenticate/usr", methods=['GET','POST'])
def authenticate():
   if request.method == 'POST':
      js = json.loads(request.data)
      print request.data
      print js['username']
      username = js['username']
      password = js['password']
      print username
      print password
      ID = auth_mobile_user(username,password)
      print ID
      resp = {}
      resp['studentID'] = ID # even though called student ID, its actually the permit code
      return json.dumps(resp)

# for user the claim a space from mobile app
@crud.route("authenticate/usr/claim_space", methods=['GET','POST'])
def try_claim():
   if request.method == 'POST':
      js = json.loads(request.data)
      print request.data
      print js['spot']
      resp = {}
      temp = 'Success'
      space_id = js['spot']
      user = js['id']
      lot_name = js['lot']
      ret_message = mobile_claim(space_id,user,lot_name)  # this mobile claim only updates the user code in a spot
      resp['status'] = ret_message
      return json.dumps(resp)

   #if request.method == 'POST':
   #   print request.data
   #   return  request.data

# [START menu]
# OLD MENU
@crud.route("Menu")
def mainMenu():
   print request.referrer
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   return render_template("index.html")
# [END menu]

# [START printQR]
@crud.route("printQR",methods=['GET','POST'])
def printQR():
   print request.referrer
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   # check for user in database, if there print it out
   if request.method == 'POST':
      firstName = request.form['fName']
      lastName = request.form['lName']
      studentID = request.form['studentID']
      permit_code = get_permit_code(studentID, firstName, lastName, 'Mobile-Users-Database')
      # if user is not in database then redirect to same page without doing anything
      if permit_code == "ID ERROR" or permit_code == "ERROR" or permit_code == "Invalid": 
         return render_template("printQR.html")
      session['qr'] = permit_code
      print "The permit code of the user is {}".format(permit_code)
      # The user is valid then redirect to print the QR code
      return redirect("printQR/image")
   return render_template("printQR.html")

# url for a generated qr image
@crud.route("printQR/image")
def display():
   print request.referrer
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   qr = session['qr']
   # a temp image genreated for the qr code, which get replaced each time
   generate_qrcode(qr,"bookshelf/static/img/temp.png")
   print qr
   # time used for browser cacheing the image
   return render_template("display_qr.html", value=qr,time=datetime.now())
  
# url for the administrater to register a user in the student permit database and mobile database  
@crud.route("Register/user", methods=['GET','POST'])
def registerUser():
   print request.referrer
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   # if user inputs fields and send post request create new user in database
   if request.method == 'POST':
      firstName = request.form['firstName']
      lastName = request.form['lastName']
      lpn = request.form['licensePlate'] #short for license plate number
      permission = request.form['permission']
      expire_days = request.form['expire_days']
      studentID = request.form['studentID']
      Name = firstName + lastName
      Code_Password = crypt(Name, lastName)
      print "Registering {} {} with license plate {} and permission {} that expires in {} days".format(firstName, lastName, lpn, permission, expire_days)

      add_student(Code_Password,firstName,lastName,lpn,Code_Password,permission,studentID, int(expire_days))
      return redirect("dashboard")
   # (re)render html page
   return render_template("regUser.html")
# [START North Remote]
@crud.route("northRemote")
def north_Remote():
   print "Trying to implement referrer"
   print request.referrer
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   
   # string to inject into html page that handles dropdown button functions
   functionCode = "<script>"
   functions = "function myFunction0001() {document.getElementById(\"myDropdown0001\").classList.toggle(\"show\");}"
   
   # string to inject into html page that handles creation of all the buttons for parking spots
   # referenced from https://www.w3schools.com/bootstrap/tryit.asp?filename=trybs_ref_js_dropdown_multilevel_css&stacked=h
   spotCode = "<div class=\"dropdown\"><button style=\"margin-left: 70px; margin-top: 110px; width: 10px; background: white;\"onclick=\"myFunction0001()\" class=\"dropbtn\"><ul id=\"myDropdown0001\" class=\"dropdown-menu\"><li><a href=\"northRemote/view0001\">view</a></li><li><a href=\"northRemote/claimSpot0001\">claim</a></li><li><a href=\"northRemote/free0001\">free</a></li><li><a href=\"northRemote/reserve0001\">reserve</a></li><li class=\"dropdown-submenu\"><a class=\"test\" tabindex=\"-1\" href=\"#\">change permission<span class=\"caret\"></span></a><ul class=\"dropdown-menu\"><li><a tabindex=\"-1\" href=\"change0001A\">A</a></li><li><a tabindex=\"-1\" href=\"change0001B\">B</a></li><li><a tabindex=\"-1\" href=\"change0001C\">C</a></li><li><a tabindex=\"-1\" href=\"change0001R\">R</a></li></div></div>"
   #northSpots = []
   #northStates = []
   #for i in range(1,100):
   #   northStates.append(i % 2)
   spotStates = lot_state('north-Remote')
   spotNumber = 1
   prevxPix = 70
   prevyPix = 110
   # position of dots on lot pages
   xPix =[100,80,95,108,120,134,150,162,176,190,
         205,220,235,249,263,278,291,305,319,333,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0
         ]
   yPix =[200,120,128,133,135,140,143,149,149,148,
         150,152,154,155,155,155,153,152,151,149,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0
         ]
   
   # loop to change color of buttons as appropraite based on state of spot
   for i in spotStates:
      if i == 1:
         spotCode = spotCode.replace("white", "green")
         spotCode = spotCode.replace("red", "green")
      elif i == 0:
         spotCode = spotCode.replace("green", "white")
         spotCode = spotCode.replace("red", "white")
      elif i == 2:
         spotCode = spotCode.replace("white", "red")
         spotCode = spotCode.replace("green", "red")
      spotCode = spotCode.replace("000" + str(spotNumber - 1), "000" + str(spotNumber))
      spotCode = spotCode.replace(str(prevxPix), str(xPix[spotNumber-1]))
      spotCode = spotCode.replace(str(prevyPix), str(yPix[spotNumber-1]))
      functions = functions.replace("000" + str(spotNumber - 1), "000" + str(spotNumber))
      
      functionCode += functions
      
      northSpots.append(Markup(spotCode))
      spotNumber += 1
      prevxPix = xPix[spotNumber-2]
      prevyPix = yPix[spotNumber-2]
   
   functionCode += "</script>"
   # if post request then change permission of all spaces in lot
   if request.method == 'POST':
      permission = u""
      checkA = request.form.get('changeA')
      checkB = request.form.get('changeB')
      checkC = request.form.get('changeC')
      checkN = request.form.get('changeN')
      checkR = request.form.get('changeR')
      if checkA:
         permission += "A"
      if checkB:
         permission += "B"
      if checkC:
         permission += "C"
      if checkN:
         permission += "R"
      change_lot_permission(permission, northRemote)
   # render html page while passing in button html code and function javascript code
   return render_template("northRemote.html",
      clickFunctions = Markup(functionCode), 
      northSpots = northSpots)
# [END North Remote]

@crud.route("/", methods=['GET','POST'])
def login():
   #add_user("Admins-Database", "admin", u"admin")
   if request.method == 'POST':
      user = request.form['uname']
      passwd = request.form['psw']
      code = auth_user(user,passwd,"Admins-Database")
      if code == "Invalid":
         return redirect("/")
      elif code:
         response = make_response(redirect("dashboard"))
         response.set_cookie("username",value=user)
         return response
  # print "I got something from student login page!!"
   return render_template("Login.html")

# [START East Remote]
@crud.route("eastRemote",  methods=['GET','POST'])
def east_Remote():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
      
   # string to inject into html page that handles dropdown button functions
   functionCode = "<script>"
   functions = "function myFunction0001() {document.getElementById(\"myDropdown0001\").classList.toggle(\"show\");}"
   
   # string to inject into html page that handles creation of all the buttons for parking spots
   # referenced from https://www.w3schools.com/bootstrap/tryit.asp?filename=trybs_ref_js_dropdown_multilevel_css&stacked=h
   spotCode = "<div class=\"dropdown\"><button style=\"margin-left: 70px; margin-top: 110px; width: 10px; background: white;\"onclick=\"myFunction0001()\" class=\"dropbtn\"><ul id=\"myDropdown0001\" class=\"dropdown-menu\"><li><a href=\"actions/eastRemote/view0001\">view</a></li><li><a href=\"actions/eastRemote/claimSpot0001\">claim</a></li><li><a href=\"actions/eastRemote/free0001\">free</a></li><li><a href=\"actions/eastRemote/reserve0001\">reserve</a></li><li class=\"dropdown-submenu\"><a class=\"test\" tabindex=\"-1\" href=\"#\">change permission<span class=\"caret\"></span></a><ul class=\"dropdown-menu\"><li><a tabindex=\"-1\" href=\"actions/eastRemote/change0001A\">A</a></li><li><a tabindex=\"-1\" href=\"actions/eastRemote/change0001B\">B</a></li><li><a tabindex=\"-1\" href=\"actions/eastRemote/change0001C\">C</a></li><li><a tabindex=\"-1\" href=\"actions/eastRemote/change0001R\">R</a></li></div></div>"
   eastSpots = []
   eastStates = []
   for i in range(1,100):
      eastStates.append(i % 2)
   spotStates = lot_state('East-Remote')
   spotNumber = 1
   prevxPix = 70
   prevyPix = 110
   # position of dots on lot pages
   xPix =[68,82,105,130,150,170,190,162,176,190,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0
         ]
   yPix =[135,135,135,135,135,135,135,135,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0
         ]
   
   # loop to change color of buttons as appropraite based on state of spot
   for i in spotStates:
      if i == 1:
         spotCode = spotCode.replace("white", "green")
         spotCode = spotCode.replace("red", "green")
      elif i == 0:
         spotCode = spotCode.replace("green", "white")
         spotCode = spotCode.replace("red", "white")
      elif i == 2:
         spotCode = spotCode.replace("white", "red")
         spotCode = spotCode.replace("green", "red")
      spotCode = spotCode.replace("000" + str(spotNumber - 1), "000" + str(spotNumber))
      spotCode = spotCode.replace(str(prevxPix), str(xPix[spotNumber-1]))
      spotCode = spotCode.replace(str(prevyPix), str(yPix[spotNumber-1]))
      functions = functions.replace("000" + str(spotNumber - 1), "000" + str(spotNumber))
      
      functionCode += functions
      
      eastSpots.append(Markup(spotCode))
      spotNumber += 1
      prevxPix = xPix[spotNumber-2]
      prevyPix = yPix[spotNumber-2]
   
   functionCode += "</script>"
   
   # if post request then change permission of all spaces in lot
   if request.method == 'POST':
      permission = u""
      checkA = request.form.get('changeA')
      checkB = request.form.get('changeB')
      checkC = request.form.get('changeC')
      checkN = request.form.get('changeN')
      checkR = request.form.get('changeR')
      if checkA:
         permission += "A"
      if checkB:
         permission += "B"
      if checkC:
         permission += "C"
      if checkN:
         permission += "N"
      if checkR:
         permission += "R"
      change_lot_permission(permission, eastRemote)
   # render html page while passing in button html code and function javascript code
   return render_template("eastRemote.html",
      clickFunctions = Markup(functionCode), 
      eastSpots = eastSpots)
# [END East Remote]

# [START West Remote]
@crud.route("westRemote", methods=['GET', 'POST'])
def west_Remote():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   
   # string to inject into html page that handles dropdown button functions
   functionCode = "<script>"
   functions = "function myFunction0001() {document.getElementById(\"myDropdown0001\").classList.toggle(\"show\");}"
   
   # string to inject into html page that handles creation of all the buttons for parking spots
   # referenced from https://www.w3schools.com/bootstrap/tryit.asp?filename=trybs_ref_js_dropdown_multilevel_css&stacked=h
   spotCode = "<div class=\"dropdown\"><button style=\"margin-left: 70px; margin-top: 110px; width: 10px; background: white;\"onclick=\"myFunction0001()\" class=\"dropbtn\"><ul id=\"myDropdown0001\" class=\"dropdown-menu\"><li><a href=\"actions/westRemote/view0001\">view</a></li><li><a href=\"actions/westRemote/claimSpot0001\">claim</a></li><li><a href=\"actions/westRemote/free0001\">free</a></li><li><a href=\"actions/westRemote/reserve0001\">reserve</a></li><li class=\"dropdown-submenu\"><a class=\"test\" tabindex=\"-1\" href=\"#\">change permission<span class=\"caret\"></span></a><ul class=\"dropdown-menu\"><li><a tabindex=\"-1\" href=\"actions/westRemote/change0001A\">A</a></li><li><a tabindex=\"-1\" href=\"actions/westRemote/change0001B\">B</a></li><li><a tabindex=\"-1\" href=\"actions/westRemote/change0001C\">C</a></li><li><a tabindex=\"-1\" href=\"actions/westRemote/change0001R\">R</a></li></div></div>"
   westSpots = []
   westStates = []
   spotStates = lot_state('West-Remote')
   spotNumber = 1
   prevxPix = 70
   prevyPix = 110
   # position of dots on lot pages
   # magic number 182 at 4th dot xpix don't put 182
   xPix =[116,137,161,183,208,230,255,276,299,324,
         345,370,395,418,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0
         ]
   yPix =[166,174,182,188,195,200,205,212,215,216,
         217,217,218,218,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,0,0
         ]
   
   for i in spotStates:
      if i == 1:
         spotCode = spotCode.replace("white", "green")
         spotCode = spotCode.replace("red", "green")
      elif i == 0:
         spotCode = spotCode.replace("green", "white")
         spotCode = spotCode.replace("red", "white")
      elif i == 2:
         spotCode = spotCode.replace("white", "red")
         spotCode = spotCode.replace("green", "red")
      spotCode = spotCode.replace("000" + str(spotNumber - 1), "000" + str(spotNumber))
      spotCode = spotCode.replace(str(prevxPix), str(xPix[spotNumber-1]))
      spotCode = spotCode.replace(str(prevyPix), str(yPix[spotNumber-1]))
      functions = functions.replace("000" + str(spotNumber - 1), "000" + str(spotNumber))
      
      functionCode += functions
      
      westSpots.append(Markup(spotCode))
      spotNumber += 1
      prevxPix = xPix[spotNumber-2]
      prevyPix = yPix[spotNumber-2]
   functionCode += "</script>"
   
   # if post request then change permission of all spaces in lot
   if request.method == 'POST':
      permission = u""
      checkA = request.form.get('changeA')
      checkB = request.form.get('changeB')
      checkC = request.form.get('changeC')
      checkN = request.form.get('changeN')
      checkR = request.form.get('changeR')
      checkU = request.form.get('changeU')
      if checkA:
         permission += "A"
      if checkB:
         permission += "B"
      if checkC:
         permission += "C"
      if checkN:
         permission += "N"
      if checkR:
         permission += "R"
      if checkU:
         permission += "U"
      change_lot_permission(permission, westRemote)
   # render html page while passing in button html code and function javascript code
   return render_template("westRemote.html",
      clickFunctions = Markup(functionCode), 
      westSpots = westSpots)
# [END West Remote]

# [START Core West]
@crud.route("Core West")
def core_West():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   return render_template("coreWest.html")
# [END Core West]

# [START logout]
@crud.route("logout")
def logout(): 
   # logout and delete cookie data
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   response = make_response(redirect("/"))
   response.set_cookie("username",expires=0) 
   return response
# [END logout]





















































"""
Here starts the QR code generator module
"""
# code that will create a QR code as called above
import pyqrcode
import sys
import png
def generate_qrcode(input_string,out_filename):
   code = pyqrcode.create(input_string)
   code.png(out_filename, scale = 12)

"""
Here starts the google cloud module
"""
# all of this code is essentially code that is copy pasted from the google cloud .py file. We were unable to properly import it from outside of the file, so we did the next best thing which was to simply paste it in.
from google.cloud import storage
from google.cloud import datastore
import os

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

# would datastore transaction be faster or
# datastore query faster ???
# I would do a experiment later!
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


def link_ble(parking_lot, spot_id, MAC):
   sensor_key = datastore_client.key("Sensor_map",unicode(MAC))
   new_sensor = datastore.Entity(key=sensor_key)
   new_sensor['Lot Name'] = unicode(parking_lot)
   new_sensor['MAC'] = unicode(MAC)
   new_sensor['spot_id'] = spot_id
   datastore_client.put(new_sensor)

def is_a_user(user_name):
   userID = 'Permit Code-{}'.format(user_name)

def query_spaces(database_name):
   query = datastore_client.query(kind=database_name)
   query.add_filter('Occupied','=',False)
   free_count = 0
   print('\n*****Start Query of Free Space*****\n')
   for space_ in query.fetch():
      free_count+=1
   new_query = datastore_client.query(kind=database_name)
   new_query.add_filter('Occupied','=',True)
   occupied_count = 0
   print('\n*****Start Query of Occupied Space*****\n')
   for space_ in new_query.fetch():
      occupied_count+=1
   return free_count, occupied_count

def lot_full_percentage(database_name):
   free, taken = query_spaces(database_name)
   quotient = ((float)(taken)/(float)(free+taken))
   percentage = quotient * 100
   return percentage
def change_passwd(code, oldpassword, newpassword):
   ID = 'Permit Code-{}'.format(code)
   #formatPass = '{}'.format(password)
   with datastore_client.transaction():
      new_key = datastore_client.key(entity_user, ID)
      student_user = datastore_client.get(new_key)
      if oldpassword == student_user['Password']:
         print ('Password match.')
         studentId = student_user['Student ID']
         print studentId
      else:
         return('Incorrect password.')
      brand_new_key = datastore_client.key(entity_mobile, studentId)
      mobile_user = datastore_client.get(brand_new_key)
      if oldpassword == mobile_user['Password']:
         print "Password match."
         student_user['Password'] = newpassword	
         mobile_user['Password'] = newpassword
         print "Password changed"
         datastore_client.put(student_user)
         datastore_client.put(mobile_user)
         return "Success"
      else:
         return "Error"

def download_blob(bucket_name, source_blob_name, destination_file_name):
   storage_client = storage.Client()
   bucket = storage_client.get_bucket(bucket_name)
   blob = bucket.blob(source_blob_name)
   blob.download_to_filename(destination_file_name)
   
   print('File {} upload to {}.'.format(source_blob_name, destination_file_name))
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


def create_lot(space_count,database_name):
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

		new_key = datastore_client.key(database_name, ID)

		# Prepares the new entity
		new_spot = datastore.Entity(key=new_key)
		new_spot['Sub-Structure'] = subStructure
		new_spot['Code'] = 0
		new_spot['License Plate'] = u'Empty'
		new_spot['Permission'] = permission
		new_spot['Occupied'] = False
		new_spot['Authorized'] = False
		new_spot['Timeframe'] = datetime.now();
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

def get_permit_code(studentID, fName, lName, database_name):
   ID = '{}'.format(studentID)
   with datastore_client.transaction():
      user_key = datastore_client.key(database_name, ID)
      if not user_key:
         return "Error"
      user = datastore_client.get(user_key)
      if not user:
         return "ID ERROR"
      if fName == user['First Name'] and lName == user['Last Name']:
         permit_code = user['Permit Code']
         return permit_code
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
def query_taken_spaces(parking_lot):
   query = datastore_client.query(kind=parking_lot)
   query.add_filter('Occupied','=', True)
   taken_spaces = 0
   for space_ in query.fetch():
      taken_spaces += 1
   return taken_spaces
def unauthorized_count(parking_lot):
   print("\n Querying the number of illegal parking in {}\n******".format(parking_lot))
   query = datastore_client.query(kind=parking_lot)
   query.add_filter('Occupied', '=', True)
   query.add_filter('Authorized','=', False)
   illegal_count = 0
   for illegal_spot in query.fetch():
      illegal_count += 1
   return illegal_count 
def active_users():
   query = datastore_client.query(kind='Student-Permit-Database')
   query.add_filter('Active', '=','1')
   n = 0
   print('\n Running Query of Active Users\n *******************\n')
   for users in query.fetch():
      n+=1
   return n


def query_spaces_count(parking_lot):
   query = datastore_client.query(kind=parking_lot)
   #query.add_filter('Occupied', '=', False)
   #query.add_filter('Occupied', '=', True)
   n = 0
   print('\nRunning Query of Spaces Count\n*************************************************\n')
   for space_ in query.fetch():
      n += 1
   print n
   return n
# end query_free_spaces()
def lot_state(parking_lot):
   start_time = datetime.now()
   free = query_spaces_count(parking_lot)
   space_states = [0] * free
   query = datastore_client.query(kind=parking_lot)
   query.add_filter('Occupied', '=', True)
   #results = list(query.fetch())
   #print results[0]
   for space in query.fetch():
      #   print space.title
      space_states[space['Space ID']-1] = 1
   query.add_filter('Authorized','=', False)
   for illegal in query.fetch():
      space_states[illegal['Space ID']-1] = 2
   finish = datetime.now()
   print finish - start_time
   return space_states
# end lot_state()

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

def read_space(parking_lot, space): #for admin to get the attributes of a parking space
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
            
            if user_:
                fname = user_['First Name']
                lname = user_['Last Name']
                student_perm = user_['Permission Level']
                student_ID = user_['Student ID']
            else:
		fname = 'Empty'
		lname = 'Empty'
		student_perm = 'Empty'
		student_ID = 'Empty'
                print('Code {} did not match any student permits'.format(code))
                #return 1
    print('Space: {}, {}, {}, {}, {}, {}, {}, {}'.format(space, authorized, student_ID, fname, lname, licPlate, student_perm, code))

    return space, authorized, student_ID, fname, lname, licPlate, student_perm, code
# end read_space()

def reset_space_defaults(space,database_name):
	RESERVE_ERROR = 0
	ID = 'Space-{}'.format(space)
	with datastore_client.transaction():
		key = datastore_client.key(database_name, ID)
		space_ = datastore_client.get(key)

		if not space_:
			RESERVE_ERROR = 1
			print('Space {} does not exist.'.format(ID))
		
		else:
			space_['Permission'] = permission
			datastore_client.put(space_)
			print('{} now has permission level {}.'.format(ID, space_['Permission']))

# end reset_space_defaults()

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
   print time_now
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

# end log_occupant()
def mobile_claim(space,code,database_name):
   ID = 'Space-{}'.format(space)
   with datastore_client.transaction():
      key = datastore_client.key(database_name, ID)
      space_ = datastore_client.get(key)
      #if space_['Occupied'] == True:
      #   if space_['Code'] == 0:
      space_permission = space_['Permission']
      if (not space_['Code'] == code) and (not space_['Code'] == 0):
         return "Occupied by other user"  
      elif space_['Code'] == code:
         return "Already Authorized"
      elif space_['Code'] == 0:   
         permit = 'Permit Code-{}'.format(code)
         student_key = datastore_client.key('Student-Permit-Database',permit)
         student = datastore_client.get(student_key)
         student_permission = student['Permission Level']
         if(student_permission > space_permission):
            return "You don't have permission to park here"
         else:
            space_['Code'] = code
            space_['Authorized'] = True # forgot the make the spot actually authorized
            datastore_client.put(space_)
            return "Success"
def claim_space(space,database_name): # accept IMAGE as well if auth == 0 the permit code is not valid
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
		key = datastore_client.key(database_name, ID)
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
					space_['Timeframe'] = datetime.now()
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
				datastore_client.put(space_)
				print('Target Space {} {} was taken'.format(space_['Sub-Structure'], space_.key.name))
				print('Permit Code {} is valid.'.format(code))

# end claim_space()

# This function is called when a car leaves a parking space and sets all the attributes of
# the space to empty or zero
def free_space(space, parking_lot):
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

def reserve_space(space,database_name):
   CLAIM_ERROR = 0;
   codeAuth = 0
   permissionLevelAuth = 0
	
   ID = 'Space-{}'.format(space)
   with datastore_client.transaction():
      key = datastore_client.key(database_name, ID)
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
         space_['Timeframe'] = datetime.now()
         datastore_client.put(space_)
         print('Target Space {} {} was taken'.format(space_['Sub-Structure'], space_.key.name))
   change_space_permission(space, u'Reserved',database_name)
   
#end reserve_space()

def change_space_permission(space, new_permission,database_name):
	RESERVE_ERROR = 0
	ID = 'Space-{}'.format(space)
	with datastore_client.transaction():
		key = datastore_client.key(database_name, ID)
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

def change_lot_permission(permission,database_name):
   CLAIM_ERROR = 0;
   codeAuth = 0
   permissionLevelAuth = 0
   space = 1
   while True:
      error = change_space_permission(space, permission,database_name)
      if error:
         break
      space += 1
# end change_lot_permission()
# This fucntion will be used by the Administrator to see how many people were parked in the parking lot
# of their choosing on a given day throughout the quarter or year
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
# end lot_statistics()
# This fucntion will be used by the Administrator to see how many people were parked in the parking lot
# of their choosing on a given day throughout the quarter or year
def log_count(hour_of_day, m, query, date):
   query.add_filter('Date', '=', date)
   query.add_filter('Hour', '=', m)
   n = 0
   for new_log in query.fetch(): #and query_hour.fetch():
      n += 1
   hour_of_day[m-8] = n
def lot_statistics_today(date):
   threads= []
   hour_of_day = [None]*13
   m = 8
   #print('\nCalculating Parking Lot Statistics\n***************************************\n')
   start = datetime.now()
   while m <= 20:
      query = datastore_client.query(kind='Log_Entity')
      t = threading.Thread(target=log_count, args=(hour_of_day,m,query,date,))
      threads.append(t)
      t.start()
      m += 1
   for t in threads:
      t.join()
   finish = datetime.now()
   print finish - start
   return hour_of_day
# end lot_statistics_today()


