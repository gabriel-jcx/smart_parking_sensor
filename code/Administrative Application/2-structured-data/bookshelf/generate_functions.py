def generate(route_name, function_name, parking_lot, space_number):
   crud_route = "@actions.route(\""
   right_brac = "\")\n"
   define = "def "
   paren = "():\n"
   static_1 = "   username = request.cookies.get(\'username\')\n"
   static_2 = "   if not username:\n"
   static_3 = "      return redirect(\"/\")\n"
   three_space = "   "
   left_brac = "("
   right_brac_without_quote = ")\n"
   ret = "   return redirect(\""
   output = crud_route+parking_lot+"/"+route_name+right_brac+define+parking_lot+route_name+paren+static_1+static_2+static_3+three_space+function_name+left_brac+space_number+","+parking_lot+right_brac_without_quote+ret+parking_lot+right_brac
   return output
def generate_permission(route_name, function_name, parking_lot, space_number,permission_level):
   crud_route = "@actions.route(\""
   right_brac = "\")\n"
   define = "def "
   paren = "():\n"
   static_1 = "   username = request.cookies.get(\'username\')\n"
   static_2 = "   if not username:\n"
   static_3 = "      return redirect(\"/\")\n"
   three_space = "   "
   left_brac = "("
   right_brac_without_quote = ")\n"
   ret = "   return redirect(\""
   output = crud_route+parking_lot+"/"+route_name+right_brac+define+parking_lot+route_name+paren+static_1+static_2+static_3+three_space+function_name+left_brac+space_number+","+"u"+"\'"+permission_level+"\',"+parking_lot+right_brac_without_quote+ret+parking_lot+right_brac
   return output
def generate_view(route_name, parking_lot, space_number):
   crud_route = "@actions.route(\""
   right_brac = "\")\n"
   define = "def "
   paren = "():\n"
   static_1 = "   username = request.cookies.get(\'username\')\n"
   static_2 = "   if not username:\n"
   static_3 = "      return redirect(\"/\")\n"
   #time = "   now = datetime.now()\n"
   read = "   space,authorized,student_ID,fName,lName,licPlate,student_perm,code=read_space("+parking_lot+","+space_number+")\n"
   image="<img src=\\\"/static/img/"+parking_lot+"_"+space_number+"_image.jpg?random={{time}}\\\">"
   table="   html_string=\"<head><style>table {font-family: arial, sans-serif;border-collapse: collapse;width: 100%;}th{text-align: center;border: 1px solid #dddddd;height: 50px;}td{border: 2px solid #dddddd;text-align: left;}tr:nth-child(even) {background-color: #dddddd;}</style></head><body><div style='float:left'><table><tr><th></th><th width=120px>Data</th><th>Photo</th></tr><tr><td> Space ID</td><td> {{space}}</td><td rowspan=\\\"8\\\">"+image+"</img></td></tr><tr><td>Authorized</td><td>{{authorized}}</td></tr><tr><td>Student ID</td><td>{{student_ID}}</td></tr><tr><td>First Name</td><td>{{fName}}</td></tr><tr><td>Last Name</td><td>{{lName}}</td></tr><tr><td>License Plate</td><td>{{licPlate}}</td></tr><tr><td>Permission Level</td><td>{{student_perm}}</td></tr><tr><td>Permit Code</td><td>{{code}}</td></tr></table></div></body>\"\n"
   print_read= "   print space,authorized,student_ID,fName,lName,student_perm\n"
   middle = "   download_blob(\"images-uploadviagateway\",\""+parking_lot+"_"+space_number+"_image.jpg\",\"bookshelf/static/img/"+parking_lot+"_"+space_number+"_image.jpg\")\n   html_head=\"<html>\"\n"+table+"   html_tail = \"</html>\"\n   f=open(\"bookshelf/templates/"+parking_lot+"_"+space_number+".html\",\"w\")\n   f.write(html_head+html_string+html_tail)\n   f.close()\n"   
   three_space = "   "
   left_brac = "("
   right_brac_without_quote = ")\n"
   ret = "   return render_template(\""
   output = crud_route+parking_lot+"/"+route_name+right_brac+define+parking_lot+route_name+paren+static_1+static_2+static_3+read+print_read+middle+ret+parking_lot+"_"+space_number+".html\",space=space,authorized=authorized,student_ID=student_ID,fName=fName,lName=lName,licPlate=licPlate,student_perm=student_perm,code=code,time=datetime.now())\n"
   return output
def Remote(space_id, lot_name):
  lot = lot_name
  claim = generate("claimSpot"+"000"+space_id,"claim_space",lot, space_id)
  free = generate("free"+"000"+space_id,"free_space",lot, space_id)
  reserve = generate("reserve"+"000"+space_id,"reserve_space",lot, space_id)
  view = generate_view("view"+"000"+space_id,lot,space_id)
  changeA = generate_permission("change"+"000"+space_id+"A","change_space_permission",lot,space_id,"A")
  changeB = generate_permission("change"+"000"+space_id+"B","change_space_permission",lot,space_id,"B")
  changeC = generate_permission("change"+"000"+space_id+"C","change_space_permission",lot,space_id,"C")
  changeR = generate_permission("change"+"000"+space_id+"R","change_space_permission",lot,space_id,"R")
  changeGuest = generate_permission("change"+"000"+space_id
  +"Guest", "change_space_permission", lot,space_id,"Guest")
  ret = claim+free+reserve+view + changeA + changeB + changeC + changeR
  return ret

f = open("new.py","w")
for i in range(1,10):
   num = str(i)
   west = Remote(num, "westRemote")
   f.write(west)
   east = Remote(num, "eastRemote")
   f.write(east)
   north = Remote(num, "northRemote")
   f.write(north)
f.close()
