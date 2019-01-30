@actions.route("westRemote/claimSpot0001")
def westRemoteclaimSpot0001():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   claim_space(1,westRemote)
   return redirect("westRemote")
@actions.route("westRemote/free0001")
def westRemotefree0001():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   free_space(1,westRemote)
   return redirect("westRemote")
@actions.route("westRemote/reserve0001")
def westRemotereserve0001():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   reserve_space(1,westRemote)
   return redirect("westRemote")
@actions.route("westRemote/view0001")
def westRemoteview0001():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   space,authorized,student_ID,fName,lName,licPlate,student_perm,code=read_space(westRemote,1)
   print space,authorized,student_ID,fName,lName,student_perm
   download_blob("images-uploadviagateway","westRemote_1_image.jpg","bookshelf/static/img/westRemote_1_image.jpg")
   html_head="<html>"
   html_string="<head><style>table {font-family: arial, sans-serif;border-collapse: collapse;width: 100%;}th{text-align: center;border: 1px solid #dddddd;height: 50px;}td{border: 2px solid #dddddd;text-align: left;}tr:nth-child(even) {background-color: #dddddd;}</style></head><body><div style='float:left'><table><tr><th></th><th width=120px>Data</th><th>Photo</th></tr><tr><td> Space ID</td><td> {{space}}</td><td rowspan=\"8\"><img src=\"/static/img/westRemote_1_image.jpg?random={{time}}\"></img></td></tr><tr><td>Authorized</td><td>{{authorized}}</td></tr><tr><td>Student ID</td><td>{{student_ID}}</td></tr><tr><td>First Name</td><td>{{fName}}</td></tr><tr><td>Last Name</td><td>{{lName}}</td></tr><tr><td>License Plate</td><td>{{licPlate}}</td></tr><tr><td>Permission Level</td><td>{{student_perm}}</td></tr><tr><td>Permit Code</td><td>Student Permit</td></tr></table></div></body>"
   html_tail = "</html>"
   f=open("bookshelf/templates/westRemote_1.html","w")
   f.write(html_head+html_string+html_tail)
   f.close()
   return render_template("westRemote_1.html",space=space,authorized=authorized,student_ID=student_ID,fName=fName,lName=lName,licPlate=licPlate,student_perm=student_perm,code=code,time=datetime.now())
@actions.route("westRemote/change0001A")
def westRemotechange0001A():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(1,u'A',westRemote)
   return redirect("westRemote")
@actions.route("westRemote/change0001B")
def westRemotechange0001B():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(1,u'B',westRemote)
   return redirect("westRemote")
@actions.route("westRemote/change0001C")
def westRemotechange0001C():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(1,u'C',westRemote)
   return redirect("westRemote")
@actions.route("westRemote/change0001R")
def westRemotechange0001R():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(1,u'R',westRemote)
   return redirect("westRemote")
@actions.route("eastRemote/claimSpot0001")
def eastRemoteclaimSpot0001():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   claim_space(1,eastRemote)
   return redirect("eastRemote")
@actions.route("eastRemote/free0001")
def eastRemotefree0001():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   free_space(1,eastRemote)
   return redirect("eastRemote")
@actions.route("eastRemote/reserve0001")
def eastRemotereserve0001():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   reserve_space(1,eastRemote)
   return redirect("eastRemote")
@actions.route("eastRemote/view0001")
def eastRemoteview0001():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   space,authorized,student_ID,fName,lName,licPlate,student_perm,code=read_space(eastRemote,1)
   print space,authorized,student_ID,fName,lName,student_perm
   download_blob("images-uploadviagateway","eastRemote_1_image.jpg","bookshelf/static/img/eastRemote_1_image.jpg")
   html_head="<html>"
   html_string="<head><style>table {font-family: arial, sans-serif;border-collapse: collapse;width: 100%;}th{text-align: center;border: 1px solid #dddddd;height: 50px;}td{border: 2px solid #dddddd;text-align: left;}tr:nth-child(even) {background-color: #dddddd;}</style></head><body><div style='float:left'><table><tr><th></th><th width=120px>Data</th><th>Photo</th></tr><tr><td> Space ID</td><td> {{space}}</td><td rowspan=\"8\"><img src=\"/static/img/eastRemote_1_image.jpg?random={{time}}\"></img></td></tr><tr><td>Authorized</td><td>{{authorized}}</td></tr><tr><td>Student ID</td><td>{{student_ID}}</td></tr><tr><td>First Name</td><td>{{fName}}</td></tr><tr><td>Last Name</td><td>{{lName}}</td></tr><tr><td>License Plate</td><td>{{licPlate}}</td></tr><tr><td>Permission Level</td><td>{{student_perm}}</td></tr><tr><td>Permit Code</td><td>Student Permit</td></tr></table></div></body>"
   html_tail = "</html>"
   f=open("bookshelf/templates/eastRemote_1.html","w")
   f.write(html_head+html_string+html_tail)
   f.close()
   return render_template("eastRemote_1.html",space=space,authorized=authorized,student_ID=student_ID,fName=fName,lName=lName,licPlate=licPlate,student_perm=student_perm,code=code,time=datetime.now())
@actions.route("eastRemote/change0001A")
def eastRemotechange0001A():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(1,u'A',eastRemote)
   return redirect("eastRemote")
@actions.route("eastRemote/change0001B")
def eastRemotechange0001B():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(1,u'B',eastRemote)
   return redirect("eastRemote")
@actions.route("eastRemote/change0001C")
def eastRemotechange0001C():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(1,u'C',eastRemote)
   return redirect("eastRemote")
@actions.route("eastRemote/change0001R")
def eastRemotechange0001R():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(1,u'R',eastRemote)
   return redirect("eastRemote")
@actions.route("northRemote/claimSpot0001")
def northRemoteclaimSpot0001():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   claim_space(1,northRemote)
   return redirect("northRemote")
@actions.route("northRemote/free0001")
def northRemotefree0001():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   free_space(1,northRemote)
   return redirect("northRemote")
@actions.route("northRemote/reserve0001")
def northRemotereserve0001():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   reserve_space(1,northRemote)
   return redirect("northRemote")
@actions.route("northRemote/view0001")
def northRemoteview0001():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   space,authorized,student_ID,fName,lName,licPlate,student_perm,code=read_space(northRemote,1)
   print space,authorized,student_ID,fName,lName,student_perm
   download_blob("images-uploadviagateway","northRemote_1_image.jpg","bookshelf/static/img/northRemote_1_image.jpg")
   html_head="<html>"
   html_string="<head><style>table {font-family: arial, sans-serif;border-collapse: collapse;width: 100%;}th{text-align: center;border: 1px solid #dddddd;height: 50px;}td{border: 2px solid #dddddd;text-align: left;}tr:nth-child(even) {background-color: #dddddd;}</style></head><body><div style='float:left'><table><tr><th></th><th width=120px>Data</th><th>Photo</th></tr><tr><td> Space ID</td><td> {{space}}</td><td rowspan=\"8\"><img src=\"/static/img/northRemote_1_image.jpg?random={{time}}\"></img></td></tr><tr><td>Authorized</td><td>{{authorized}}</td></tr><tr><td>Student ID</td><td>{{student_ID}}</td></tr><tr><td>First Name</td><td>{{fName}}</td></tr><tr><td>Last Name</td><td>{{lName}}</td></tr><tr><td>License Plate</td><td>{{licPlate}}</td></tr><tr><td>Permission Level</td><td>{{student_perm}}</td></tr><tr><td>Permit Code</td><td>Student Permit</td></tr></table></div></body>"
   html_tail = "</html>"
   f=open("bookshelf/templates/northRemote_1.html","w")
   f.write(html_head+html_string+html_tail)
   f.close()
   return render_template("northRemote_1.html",space=space,authorized=authorized,student_ID=student_ID,fName=fName,lName=lName,licPlate=licPlate,student_perm=student_perm,code=code,time=datetime.now())
@actions.route("northRemote/change0001A")
def northRemotechange0001A():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(1,u'A',northRemote)
   return redirect("northRemote")
@actions.route("northRemote/change0001B")
def northRemotechange0001B():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(1,u'B',northRemote)
   return redirect("northRemote")
@actions.route("northRemote/change0001C")
def northRemotechange0001C():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(1,u'C',northRemote)
   return redirect("northRemote")
@actions.route("northRemote/change0001R")
def northRemotechange0001R():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(1,u'R',northRemote)
   return redirect("northRemote")
@actions.route("westRemote/claimSpot0002")
def westRemoteclaimSpot0002():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   claim_space(2,westRemote)
   return redirect("westRemote")
@actions.route("westRemote/free0002")
def westRemotefree0002():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   free_space(2,westRemote)
   return redirect("westRemote")
@actions.route("westRemote/reserve0002")
def westRemotereserve0002():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   reserve_space(2,westRemote)
   return redirect("westRemote")
@actions.route("westRemote/view0002")
def westRemoteview0002():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   space,authorized,student_ID,fName,lName,licPlate,student_perm,code=read_space(westRemote,2)
   print space,authorized,student_ID,fName,lName,student_perm
   download_blob("images-uploadviagateway","westRemote_2_image.jpg","bookshelf/static/img/westRemote_2_image.jpg")
   html_head="<html>"
   html_string="<head><style>table {font-family: arial, sans-serif;border-collapse: collapse;width: 100%;}th{text-align: center;border: 1px solid #dddddd;height: 50px;}td{border: 2px solid #dddddd;text-align: left;}tr:nth-child(even) {background-color: #dddddd;}</style></head><body><div style='float:left'><table><tr><th></th><th width=120px>Data</th><th>Photo</th></tr><tr><td> Space ID</td><td> {{space}}</td><td rowspan=\"8\"><img src=\"/static/img/westRemote_2_image.jpg?random={{time}}\"></img></td></tr><tr><td>Authorized</td><td>{{authorized}}</td></tr><tr><td>Student ID</td><td>{{student_ID}}</td></tr><tr><td>First Name</td><td>{{fName}}</td></tr><tr><td>Last Name</td><td>{{lName}}</td></tr><tr><td>License Plate</td><td>{{licPlate}}</td></tr><tr><td>Permission Level</td><td>{{student_perm}}</td></tr><tr><td>Permit Code</td><td>Student Permit</td></tr></table></div></body>"
   html_tail = "</html>"
   f=open("bookshelf/templates/westRemote_2.html","w")
   f.write(html_head+html_string+html_tail)
   f.close()
   return render_template("westRemote_2.html",space=space,authorized=authorized,student_ID=student_ID,fName=fName,lName=lName,licPlate=licPlate,student_perm=student_perm,code=code,time=datetime.now())
@actions.route("westRemote/change0002A")
def westRemotechange0002A():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(2,u'A',westRemote)
   return redirect("westRemote")
@actions.route("westRemote/change0002B")
def westRemotechange0002B():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(2,u'B',westRemote)
   return redirect("westRemote")
@actions.route("westRemote/change0002C")
def westRemotechange0002C():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(2,u'C',westRemote)
   return redirect("westRemote")
@actions.route("westRemote/change0002R")
def westRemotechange0002R():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(2,u'R',westRemote)
   return redirect("westRemote")
@actions.route("eastRemote/claimSpot0002")
def eastRemoteclaimSpot0002():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   claim_space(2,eastRemote)
   return redirect("eastRemote")
@actions.route("eastRemote/free0002")
def eastRemotefree0002():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   free_space(2,eastRemote)
   return redirect("eastRemote")
@actions.route("eastRemote/reserve0002")
def eastRemotereserve0002():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   reserve_space(2,eastRemote)
   return redirect("eastRemote")
@actions.route("eastRemote/view0002")
def eastRemoteview0002():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   space,authorized,student_ID,fName,lName,licPlate,student_perm,code=read_space(eastRemote,2)
   print space,authorized,student_ID,fName,lName,student_perm
   download_blob("images-uploadviagateway","eastRemote_2_image.jpg","bookshelf/static/img/eastRemote_2_image.jpg")
   html_head="<html>"
   html_string="<head><style>table {font-family: arial, sans-serif;border-collapse: collapse;width: 100%;}th{text-align: center;border: 1px solid #dddddd;height: 50px;}td{border: 2px solid #dddddd;text-align: left;}tr:nth-child(even) {background-color: #dddddd;}</style></head><body><div style='float:left'><table><tr><th></th><th width=120px>Data</th><th>Photo</th></tr><tr><td> Space ID</td><td> {{space}}</td><td rowspan=\"8\"><img src=\"/static/img/eastRemote_2_image.jpg?random={{time}}\"></img></td></tr><tr><td>Authorized</td><td>{{authorized}}</td></tr><tr><td>Student ID</td><td>{{student_ID}}</td></tr><tr><td>First Name</td><td>{{fName}}</td></tr><tr><td>Last Name</td><td>{{lName}}</td></tr><tr><td>License Plate</td><td>{{licPlate}}</td></tr><tr><td>Permission Level</td><td>{{student_perm}}</td></tr><tr><td>Permit Code</td><td>Student Permit</td></tr></table></div></body>"
   html_tail = "</html>"
   f=open("bookshelf/templates/eastRemote_2.html","w")
   f.write(html_head+html_string+html_tail)
   f.close()
   return render_template("eastRemote_2.html",space=space,authorized=authorized,student_ID=student_ID,fName=fName,lName=lName,licPlate=licPlate,student_perm=student_perm,code=code,time=datetime.now())
@actions.route("eastRemote/change0002A")
def eastRemotechange0002A():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(2,u'A',eastRemote)
   return redirect("eastRemote")
@actions.route("eastRemote/change0002B")
def eastRemotechange0002B():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(2,u'B',eastRemote)
   return redirect("eastRemote")
@actions.route("eastRemote/change0002C")
def eastRemotechange0002C():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(2,u'C',eastRemote)
   return redirect("eastRemote")
@actions.route("eastRemote/change0002R")
def eastRemotechange0002R():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(2,u'R',eastRemote)
   return redirect("eastRemote")
@actions.route("northRemote/claimSpot0002")
def northRemoteclaimSpot0002():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   claim_space(2,northRemote)
   return redirect("northRemote")
@actions.route("northRemote/free0002")
def northRemotefree0002():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   free_space(2,northRemote)
   return redirect("northRemote")
@actions.route("northRemote/reserve0002")
def northRemotereserve0002():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   reserve_space(2,northRemote)
   return redirect("northRemote")
@actions.route("northRemote/view0002")
def northRemoteview0002():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   space,authorized,student_ID,fName,lName,licPlate,student_perm,code=read_space(northRemote,2)
   print space,authorized,student_ID,fName,lName,student_perm
   download_blob("images-uploadviagateway","northRemote_2_image.jpg","bookshelf/static/img/northRemote_2_image.jpg")
   html_head="<html>"
   html_string="<head><style>table {font-family: arial, sans-serif;border-collapse: collapse;width: 100%;}th{text-align: center;border: 1px solid #dddddd;height: 50px;}td{border: 2px solid #dddddd;text-align: left;}tr:nth-child(even) {background-color: #dddddd;}</style></head><body><div style='float:left'><table><tr><th></th><th width=120px>Data</th><th>Photo</th></tr><tr><td> Space ID</td><td> {{space}}</td><td rowspan=\"8\"><img src=\"/static/img/northRemote_2_image.jpg?random={{time}}\"></img></td></tr><tr><td>Authorized</td><td>{{authorized}}</td></tr><tr><td>Student ID</td><td>{{student_ID}}</td></tr><tr><td>First Name</td><td>{{fName}}</td></tr><tr><td>Last Name</td><td>{{lName}}</td></tr><tr><td>License Plate</td><td>{{licPlate}}</td></tr><tr><td>Permission Level</td><td>{{student_perm}}</td></tr><tr><td>Permit Code</td><td>Student Permit</td></tr></table></div></body>"
   html_tail = "</html>"
   f=open("bookshelf/templates/northRemote_2.html","w")
   f.write(html_head+html_string+html_tail)
   f.close()
   return render_template("northRemote_2.html",space=space,authorized=authorized,student_ID=student_ID,fName=fName,lName=lName,licPlate=licPlate,student_perm=student_perm,code=code,time=datetime.now())
@actions.route("northRemote/change0002A")
def northRemotechange0002A():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(2,u'A',northRemote)
   return redirect("northRemote")
@actions.route("northRemote/change0002B")
def northRemotechange0002B():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(2,u'B',northRemote)
   return redirect("northRemote")
@actions.route("northRemote/change0002C")
def northRemotechange0002C():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(2,u'C',northRemote)
   return redirect("northRemote")
@actions.route("northRemote/change0002R")
def northRemotechange0002R():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(2,u'R',northRemote)
   return redirect("northRemote")
@actions.route("westRemote/claimSpot0003")
def westRemoteclaimSpot0003():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   claim_space(3,westRemote)
   return redirect("westRemote")
@actions.route("westRemote/free0003")
def westRemotefree0003():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   free_space(3,westRemote)
   return redirect("westRemote")
@actions.route("westRemote/reserve0003")
def westRemotereserve0003():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   reserve_space(3,westRemote)
   return redirect("westRemote")
@actions.route("westRemote/view0003")
def westRemoteview0003():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   space,authorized,student_ID,fName,lName,licPlate,student_perm,code=read_space(westRemote,3)
   print space,authorized,student_ID,fName,lName,student_perm
   download_blob("images-uploadviagateway","westRemote_3_image.jpg","bookshelf/static/img/westRemote_3_image.jpg")
   html_head="<html>"
   html_string="<head><style>table {font-family: arial, sans-serif;border-collapse: collapse;width: 100%;}th{text-align: center;border: 1px solid #dddddd;height: 50px;}td{border: 2px solid #dddddd;text-align: left;}tr:nth-child(even) {background-color: #dddddd;}</style></head><body><div style='float:left'><table><tr><th></th><th width=120px>Data</th><th>Photo</th></tr><tr><td> Space ID</td><td> {{space}}</td><td rowspan=\"8\"><img src=\"/static/img/westRemote_3_image.jpg?random={{time}}\"></img></td></tr><tr><td>Authorized</td><td>{{authorized}}</td></tr><tr><td>Student ID</td><td>{{student_ID}}</td></tr><tr><td>First Name</td><td>{{fName}}</td></tr><tr><td>Last Name</td><td>{{lName}}</td></tr><tr><td>License Plate</td><td>{{licPlate}}</td></tr><tr><td>Permission Level</td><td>{{student_perm}}</td></tr><tr><td>Permit Code</td><td>Student Permit</td></tr></table></div></body>"
   html_tail = "</html>"
   f=open("bookshelf/templates/westRemote_3.html","w")
   f.write(html_head+html_string+html_tail)
   f.close()
   return render_template("westRemote_3.html",space=space,authorized=authorized,student_ID=student_ID,fName=fName,lName=lName,licPlate=licPlate,student_perm=student_perm,code=code,time=datetime.now())
@actions.route("westRemote/change0003A")
def westRemotechange0003A():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(3,u'A',westRemote)
   return redirect("westRemote")
@actions.route("westRemote/change0003B")
def westRemotechange0003B():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(3,u'B',westRemote)
   return redirect("westRemote")
@actions.route("westRemote/change0003C")
def westRemotechange0003C():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(3,u'C',westRemote)
   return redirect("westRemote")
@actions.route("westRemote/change0003R")
def westRemotechange0003R():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(3,u'R',westRemote)
   return redirect("westRemote")
@actions.route("eastRemote/claimSpot0003")
def eastRemoteclaimSpot0003():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   claim_space(3,eastRemote)
   return redirect("eastRemote")
@actions.route("eastRemote/free0003")
def eastRemotefree0003():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   free_space(3,eastRemote)
   return redirect("eastRemote")
@actions.route("eastRemote/reserve0003")
def eastRemotereserve0003():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   reserve_space(3,eastRemote)
   return redirect("eastRemote")
@actions.route("eastRemote/view0003")
def eastRemoteview0003():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   space,authorized,student_ID,fName,lName,licPlate,student_perm,code=read_space(eastRemote,3)
   print space,authorized,student_ID,fName,lName,student_perm
   download_blob("images-uploadviagateway","eastRemote_3_image.jpg","bookshelf/static/img/eastRemote_3_image.jpg")
   html_head="<html>"
   html_string="<head><style>table {font-family: arial, sans-serif;border-collapse: collapse;width: 100%;}th{text-align: center;border: 1px solid #dddddd;height: 50px;}td{border: 2px solid #dddddd;text-align: left;}tr:nth-child(even) {background-color: #dddddd;}</style></head><body><div style='float:left'><table><tr><th></th><th width=120px>Data</th><th>Photo</th></tr><tr><td> Space ID</td><td> {{space}}</td><td rowspan=\"8\"><img src=\"/static/img/eastRemote_3_image.jpg?random={{time}}\"></img></td></tr><tr><td>Authorized</td><td>{{authorized}}</td></tr><tr><td>Student ID</td><td>{{student_ID}}</td></tr><tr><td>First Name</td><td>{{fName}}</td></tr><tr><td>Last Name</td><td>{{lName}}</td></tr><tr><td>License Plate</td><td>{{licPlate}}</td></tr><tr><td>Permission Level</td><td>{{student_perm}}</td></tr><tr><td>Permit Code</td><td>Student Permit</td></tr></table></div></body>"
   html_tail = "</html>"
   f=open("bookshelf/templates/eastRemote_3.html","w")
   f.write(html_head+html_string+html_tail)
   f.close()
   return render_template("eastRemote_3.html",space=space,authorized=authorized,student_ID=student_ID,fName=fName,lName=lName,licPlate=licPlate,student_perm=student_perm,code=code,time=datetime.now())
@actions.route("eastRemote/change0003A")
def eastRemotechange0003A():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(3,u'A',eastRemote)
   return redirect("eastRemote")
@actions.route("eastRemote/change0003B")
def eastRemotechange0003B():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(3,u'B',eastRemote)
   return redirect("eastRemote")
@actions.route("eastRemote/change0003C")
def eastRemotechange0003C():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(3,u'C',eastRemote)
   return redirect("eastRemote")
@actions.route("eastRemote/change0003R")
def eastRemotechange0003R():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(3,u'R',eastRemote)
   return redirect("eastRemote")
@actions.route("northRemote/claimSpot0003")
def northRemoteclaimSpot0003():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   claim_space(3,northRemote)
   return redirect("northRemote")
@actions.route("northRemote/free0003")
def northRemotefree0003():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   free_space(3,northRemote)
   return redirect("northRemote")
@actions.route("northRemote/reserve0003")
def northRemotereserve0003():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   reserve_space(3,northRemote)
   return redirect("northRemote")
@actions.route("northRemote/view0003")
def northRemoteview0003():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   space,authorized,student_ID,fName,lName,licPlate,student_perm,code=read_space(northRemote,3)
   print space,authorized,student_ID,fName,lName,student_perm
   download_blob("images-uploadviagateway","northRemote_3_image.jpg","bookshelf/static/img/northRemote_3_image.jpg")
   html_head="<html>"
   html_string="<head><style>table {font-family: arial, sans-serif;border-collapse: collapse;width: 100%;}th{text-align: center;border: 1px solid #dddddd;height: 50px;}td{border: 2px solid #dddddd;text-align: left;}tr:nth-child(even) {background-color: #dddddd;}</style></head><body><div style='float:left'><table><tr><th></th><th width=120px>Data</th><th>Photo</th></tr><tr><td> Space ID</td><td> {{space}}</td><td rowspan=\"8\"><img src=\"/static/img/northRemote_3_image.jpg?random={{time}}\"></img></td></tr><tr><td>Authorized</td><td>{{authorized}}</td></tr><tr><td>Student ID</td><td>{{student_ID}}</td></tr><tr><td>First Name</td><td>{{fName}}</td></tr><tr><td>Last Name</td><td>{{lName}}</td></tr><tr><td>License Plate</td><td>{{licPlate}}</td></tr><tr><td>Permission Level</td><td>{{student_perm}}</td></tr><tr><td>Permit Code</td><td>Student Permit</td></tr></table></div></body>"
   html_tail = "</html>"
   f=open("bookshelf/templates/northRemote_3.html","w")
   f.write(html_head+html_string+html_tail)
   f.close()
   return render_template("northRemote_3.html",space=space,authorized=authorized,student_ID=student_ID,fName=fName,lName=lName,licPlate=licPlate,student_perm=student_perm,code=code,time=datetime.now())
@actions.route("northRemote/change0003A")
def northRemotechange0003A():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(3,u'A',northRemote)
   return redirect("northRemote")
@actions.route("northRemote/change0003B")
def northRemotechange0003B():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(3,u'B',northRemote)
   return redirect("northRemote")
@actions.route("northRemote/change0003C")
def northRemotechange0003C():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(3,u'C',northRemote)
   return redirect("northRemote")
@actions.route("northRemote/change0003R")
def northRemotechange0003R():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(3,u'R',northRemote)
   return redirect("northRemote")
@actions.route("westRemote/claimSpot0004")
def westRemoteclaimSpot0004():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   claim_space(4,westRemote)
   return redirect("westRemote")
@actions.route("westRemote/free0004")
def westRemotefree0004():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   free_space(4,westRemote)
   return redirect("westRemote")
@actions.route("westRemote/reserve0004")
def westRemotereserve0004():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   reserve_space(4,westRemote)
   return redirect("westRemote")
@actions.route("westRemote/view0004")
def westRemoteview0004():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   space,authorized,student_ID,fName,lName,licPlate,student_perm,code=read_space(westRemote,4)
   print space,authorized,student_ID,fName,lName,student_perm
   download_blob("images-uploadviagateway","westRemote_4_image.jpg","bookshelf/static/img/westRemote_4_image.jpg")
   html_head="<html>"
   html_string="<head><style>table {font-family: arial, sans-serif;border-collapse: collapse;width: 100%;}th{text-align: center;border: 1px solid #dddddd;height: 50px;}td{border: 2px solid #dddddd;text-align: left;}tr:nth-child(even) {background-color: #dddddd;}</style></head><body><div style='float:left'><table><tr><th></th><th width=120px>Data</th><th>Photo</th></tr><tr><td> Space ID</td><td> {{space}}</td><td rowspan=\"8\"><img src=\"/static/img/westRemote_4_image.jpg?random={{time}}\"></img></td></tr><tr><td>Authorized</td><td>{{authorized}}</td></tr><tr><td>Student ID</td><td>{{student_ID}}</td></tr><tr><td>First Name</td><td>{{fName}}</td></tr><tr><td>Last Name</td><td>{{lName}}</td></tr><tr><td>License Plate</td><td>{{licPlate}}</td></tr><tr><td>Permission Level</td><td>{{student_perm}}</td></tr><tr><td>Permit Code</td><td>Student Permit</td></tr></table></div></body>"
   html_tail = "</html>"
   f=open("bookshelf/templates/westRemote_4.html","w")
   f.write(html_head+html_string+html_tail)
   f.close()
   return render_template("westRemote_4.html",space=space,authorized=authorized,student_ID=student_ID,fName=fName,lName=lName,licPlate=licPlate,student_perm=student_perm,code=code,time=datetime.now())
@actions.route("westRemote/change0004A")
def westRemotechange0004A():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(4,u'A',westRemote)
   return redirect("westRemote")
@actions.route("westRemote/change0004B")
def westRemotechange0004B():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(4,u'B',westRemote)
   return redirect("westRemote")
@actions.route("westRemote/change0004C")
def westRemotechange0004C():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(4,u'C',westRemote)
   return redirect("westRemote")
@actions.route("westRemote/change0004R")
def westRemotechange0004R():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(4,u'R',westRemote)
   return redirect("westRemote")
@actions.route("eastRemote/claimSpot0004")
def eastRemoteclaimSpot0004():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   claim_space(4,eastRemote)
   return redirect("eastRemote")
@actions.route("eastRemote/free0004")
def eastRemotefree0004():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   free_space(4,eastRemote)
   return redirect("eastRemote")
@actions.route("eastRemote/reserve0004")
def eastRemotereserve0004():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   reserve_space(4,eastRemote)
   return redirect("eastRemote")
@actions.route("eastRemote/view0004")
def eastRemoteview0004():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   space,authorized,student_ID,fName,lName,licPlate,student_perm,code=read_space(eastRemote,4)
   print space,authorized,student_ID,fName,lName,student_perm
   download_blob("images-uploadviagateway","eastRemote_4_image.jpg","bookshelf/static/img/eastRemote_4_image.jpg")
   html_head="<html>"
   html_string="<head><style>table {font-family: arial, sans-serif;border-collapse: collapse;width: 100%;}th{text-align: center;border: 1px solid #dddddd;height: 50px;}td{border: 2px solid #dddddd;text-align: left;}tr:nth-child(even) {background-color: #dddddd;}</style></head><body><div style='float:left'><table><tr><th></th><th width=120px>Data</th><th>Photo</th></tr><tr><td> Space ID</td><td> {{space}}</td><td rowspan=\"8\"><img src=\"/static/img/eastRemote_4_image.jpg?random={{time}}\"></img></td></tr><tr><td>Authorized</td><td>{{authorized}}</td></tr><tr><td>Student ID</td><td>{{student_ID}}</td></tr><tr><td>First Name</td><td>{{fName}}</td></tr><tr><td>Last Name</td><td>{{lName}}</td></tr><tr><td>License Plate</td><td>{{licPlate}}</td></tr><tr><td>Permission Level</td><td>{{student_perm}}</td></tr><tr><td>Permit Code</td><td>Student Permit</td></tr></table></div></body>"
   html_tail = "</html>"
   f=open("bookshelf/templates/eastRemote_4.html","w")
   f.write(html_head+html_string+html_tail)
   f.close()
   return render_template("eastRemote_4.html",space=space,authorized=authorized,student_ID=student_ID,fName=fName,lName=lName,licPlate=licPlate,student_perm=student_perm,code=code,time=datetime.now())
@actions.route("eastRemote/change0004A")
def eastRemotechange0004A():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(4,u'A',eastRemote)
   return redirect("eastRemote")
@actions.route("eastRemote/change0004B")
def eastRemotechange0004B():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(4,u'B',eastRemote)
   return redirect("eastRemote")
@actions.route("eastRemote/change0004C")
def eastRemotechange0004C():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(4,u'C',eastRemote)
   return redirect("eastRemote")
@actions.route("eastRemote/change0004R")
def eastRemotechange0004R():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(4,u'R',eastRemote)
   return redirect("eastRemote")
@actions.route("northRemote/claimSpot0004")
def northRemoteclaimSpot0004():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   claim_space(4,northRemote)
   return redirect("northRemote")
@actions.route("northRemote/free0004")
def northRemotefree0004():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   free_space(4,northRemote)
   return redirect("northRemote")
@actions.route("northRemote/reserve0004")
def northRemotereserve0004():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   reserve_space(4,northRemote)
   return redirect("northRemote")
@actions.route("northRemote/view0004")
def northRemoteview0004():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   space,authorized,student_ID,fName,lName,licPlate,student_perm,code=read_space(northRemote,4)
   print space,authorized,student_ID,fName,lName,student_perm
   download_blob("images-uploadviagateway","northRemote_4_image.jpg","bookshelf/static/img/northRemote_4_image.jpg")
   html_head="<html>"
   html_string="<head><style>table {font-family: arial, sans-serif;border-collapse: collapse;width: 100%;}th{text-align: center;border: 1px solid #dddddd;height: 50px;}td{border: 2px solid #dddddd;text-align: left;}tr:nth-child(even) {background-color: #dddddd;}</style></head><body><div style='float:left'><table><tr><th></th><th width=120px>Data</th><th>Photo</th></tr><tr><td> Space ID</td><td> {{space}}</td><td rowspan=\"8\"><img src=\"/static/img/northRemote_4_image.jpg?random={{time}}\"></img></td></tr><tr><td>Authorized</td><td>{{authorized}}</td></tr><tr><td>Student ID</td><td>{{student_ID}}</td></tr><tr><td>First Name</td><td>{{fName}}</td></tr><tr><td>Last Name</td><td>{{lName}}</td></tr><tr><td>License Plate</td><td>{{licPlate}}</td></tr><tr><td>Permission Level</td><td>{{student_perm}}</td></tr><tr><td>Permit Code</td><td>Student Permit</td></tr></table></div></body>"
   html_tail = "</html>"
   f=open("bookshelf/templates/northRemote_4.html","w")
   f.write(html_head+html_string+html_tail)
   f.close()
   return render_template("northRemote_4.html",space=space,authorized=authorized,student_ID=student_ID,fName=fName,lName=lName,licPlate=licPlate,student_perm=student_perm,code=code,time=datetime.now())
@actions.route("northRemote/change0004A")
def northRemotechange0004A():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(4,u'A',northRemote)
   return redirect("northRemote")
@actions.route("northRemote/change0004B")
def northRemotechange0004B():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(4,u'B',northRemote)
   return redirect("northRemote")
@actions.route("northRemote/change0004C")
def northRemotechange0004C():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(4,u'C',northRemote)
   return redirect("northRemote")
@actions.route("northRemote/change0004R")
def northRemotechange0004R():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(4,u'R',northRemote)
   return redirect("northRemote")
@actions.route("westRemote/claimSpot0005")
def westRemoteclaimSpot0005():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   claim_space(5,westRemote)
   return redirect("westRemote")
@actions.route("westRemote/free0005")
def westRemotefree0005():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   free_space(5,westRemote)
   return redirect("westRemote")
@actions.route("westRemote/reserve0005")
def westRemotereserve0005():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   reserve_space(5,westRemote)
   return redirect("westRemote")
@actions.route("westRemote/view0005")
def westRemoteview0005():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   space,authorized,student_ID,fName,lName,licPlate,student_perm,code=read_space(westRemote,5)
   print space,authorized,student_ID,fName,lName,student_perm
   download_blob("images-uploadviagateway","westRemote_5_image.jpg","bookshelf/static/img/westRemote_5_image.jpg")
   html_head="<html>"
   html_string="<head><style>table {font-family: arial, sans-serif;border-collapse: collapse;width: 100%;}th{text-align: center;border: 1px solid #dddddd;height: 50px;}td{border: 2px solid #dddddd;text-align: left;}tr:nth-child(even) {background-color: #dddddd;}</style></head><body><div style='float:left'><table><tr><th></th><th width=120px>Data</th><th>Photo</th></tr><tr><td> Space ID</td><td> {{space}}</td><td rowspan=\"8\"><img src=\"/static/img/westRemote_5_image.jpg?random={{time}}\"></img></td></tr><tr><td>Authorized</td><td>{{authorized}}</td></tr><tr><td>Student ID</td><td>{{student_ID}}</td></tr><tr><td>First Name</td><td>{{fName}}</td></tr><tr><td>Last Name</td><td>{{lName}}</td></tr><tr><td>License Plate</td><td>{{licPlate}}</td></tr><tr><td>Permission Level</td><td>{{student_perm}}</td></tr><tr><td>Permit Code</td><td>Student Permit</td></tr></table></div></body>"
   html_tail = "</html>"
   f=open("bookshelf/templates/westRemote_5.html","w")
   f.write(html_head+html_string+html_tail)
   f.close()
   return render_template("westRemote_5.html",space=space,authorized=authorized,student_ID=student_ID,fName=fName,lName=lName,licPlate=licPlate,student_perm=student_perm,code=code,time=datetime.now())
@actions.route("westRemote/change0005A")
def westRemotechange0005A():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(5,u'A',westRemote)
   return redirect("westRemote")
@actions.route("westRemote/change0005B")
def westRemotechange0005B():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(5,u'B',westRemote)
   return redirect("westRemote")
@actions.route("westRemote/change0005C")
def westRemotechange0005C():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(5,u'C',westRemote)
   return redirect("westRemote")
@actions.route("westRemote/change0005R")
def westRemotechange0005R():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(5,u'R',westRemote)
   return redirect("westRemote")
@actions.route("eastRemote/claimSpot0005")
def eastRemoteclaimSpot0005():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   claim_space(5,eastRemote)
   return redirect("eastRemote")
@actions.route("eastRemote/free0005")
def eastRemotefree0005():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   free_space(5,eastRemote)
   return redirect("eastRemote")
@actions.route("eastRemote/reserve0005")
def eastRemotereserve0005():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   reserve_space(5,eastRemote)
   return redirect("eastRemote")
@actions.route("eastRemote/view0005")
def eastRemoteview0005():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   space,authorized,student_ID,fName,lName,licPlate,student_perm,code=read_space(eastRemote,5)
   print space,authorized,student_ID,fName,lName,student_perm
   download_blob("images-uploadviagateway","eastRemote_5_image.jpg","bookshelf/static/img/eastRemote_5_image.jpg")
   html_head="<html>"
   html_string="<head><style>table {font-family: arial, sans-serif;border-collapse: collapse;width: 100%;}th{text-align: center;border: 1px solid #dddddd;height: 50px;}td{border: 2px solid #dddddd;text-align: left;}tr:nth-child(even) {background-color: #dddddd;}</style></head><body><div style='float:left'><table><tr><th></th><th width=120px>Data</th><th>Photo</th></tr><tr><td> Space ID</td><td> {{space}}</td><td rowspan=\"8\"><img src=\"/static/img/eastRemote_5_image.jpg?random={{time}}\"></img></td></tr><tr><td>Authorized</td><td>{{authorized}}</td></tr><tr><td>Student ID</td><td>{{student_ID}}</td></tr><tr><td>First Name</td><td>{{fName}}</td></tr><tr><td>Last Name</td><td>{{lName}}</td></tr><tr><td>License Plate</td><td>{{licPlate}}</td></tr><tr><td>Permission Level</td><td>{{student_perm}}</td></tr><tr><td>Permit Code</td><td>Student Permit</td></tr></table></div></body>"
   html_tail = "</html>"
   f=open("bookshelf/templates/eastRemote_5.html","w")
   f.write(html_head+html_string+html_tail)
   f.close()
   return render_template("eastRemote_5.html",space=space,authorized=authorized,student_ID=student_ID,fName=fName,lName=lName,licPlate=licPlate,student_perm=student_perm,code=code,time=datetime.now())
@actions.route("eastRemote/change0005A")
def eastRemotechange0005A():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(5,u'A',eastRemote)
   return redirect("eastRemote")
@actions.route("eastRemote/change0005B")
def eastRemotechange0005B():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(5,u'B',eastRemote)
   return redirect("eastRemote")
@actions.route("eastRemote/change0005C")
def eastRemotechange0005C():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(5,u'C',eastRemote)
   return redirect("eastRemote")
@actions.route("eastRemote/change0005R")
def eastRemotechange0005R():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(5,u'R',eastRemote)
   return redirect("eastRemote")
@actions.route("northRemote/claimSpot0005")
def northRemoteclaimSpot0005():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   claim_space(5,northRemote)
   return redirect("northRemote")
@actions.route("northRemote/free0005")
def northRemotefree0005():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   free_space(5,northRemote)
   return redirect("northRemote")
@actions.route("northRemote/reserve0005")
def northRemotereserve0005():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   reserve_space(5,northRemote)
   return redirect("northRemote")
@actions.route("northRemote/view0005")
def northRemoteview0005():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   space,authorized,student_ID,fName,lName,licPlate,student_perm,code=read_space(northRemote,5)
   print space,authorized,student_ID,fName,lName,student_perm
   download_blob("images-uploadviagateway","northRemote_5_image.jpg","bookshelf/static/img/northRemote_5_image.jpg")
   html_head="<html>"
   html_string="<head><style>table {font-family: arial, sans-serif;border-collapse: collapse;width: 100%;}th{text-align: center;border: 1px solid #dddddd;height: 50px;}td{border: 2px solid #dddddd;text-align: left;}tr:nth-child(even) {background-color: #dddddd;}</style></head><body><div style='float:left'><table><tr><th></th><th width=120px>Data</th><th>Photo</th></tr><tr><td> Space ID</td><td> {{space}}</td><td rowspan=\"8\"><img src=\"/static/img/northRemote_5_image.jpg?random={{time}}\"></img></td></tr><tr><td>Authorized</td><td>{{authorized}}</td></tr><tr><td>Student ID</td><td>{{student_ID}}</td></tr><tr><td>First Name</td><td>{{fName}}</td></tr><tr><td>Last Name</td><td>{{lName}}</td></tr><tr><td>License Plate</td><td>{{licPlate}}</td></tr><tr><td>Permission Level</td><td>{{student_perm}}</td></tr><tr><td>Permit Code</td><td>Student Permit</td></tr></table></div></body>"
   html_tail = "</html>"
   f=open("bookshelf/templates/northRemote_5.html","w")
   f.write(html_head+html_string+html_tail)
   f.close()
   return render_template("northRemote_5.html",space=space,authorized=authorized,student_ID=student_ID,fName=fName,lName=lName,licPlate=licPlate,student_perm=student_perm,code=code,time=datetime.now())
@actions.route("northRemote/change0005A")
def northRemotechange0005A():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(5,u'A',northRemote)
   return redirect("northRemote")
@actions.route("northRemote/change0005B")
def northRemotechange0005B():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(5,u'B',northRemote)
   return redirect("northRemote")
@actions.route("northRemote/change0005C")
def northRemotechange0005C():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(5,u'C',northRemote)
   return redirect("northRemote")
@actions.route("northRemote/change0005R")
def northRemotechange0005R():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(5,u'R',northRemote)
   return redirect("northRemote")
@actions.route("westRemote/claimSpot0006")
def westRemoteclaimSpot0006():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   claim_space(6,westRemote)
   return redirect("westRemote")
@actions.route("westRemote/free0006")
def westRemotefree0006():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   free_space(6,westRemote)
   return redirect("westRemote")
@actions.route("westRemote/reserve0006")
def westRemotereserve0006():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   reserve_space(6,westRemote)
   return redirect("westRemote")
@actions.route("westRemote/view0006")
def westRemoteview0006():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   space,authorized,student_ID,fName,lName,licPlate,student_perm,code=read_space(westRemote,6)
   print space,authorized,student_ID,fName,lName,student_perm
   download_blob("images-uploadviagateway","westRemote_6_image.jpg","bookshelf/static/img/westRemote_6_image.jpg")
   html_head="<html>"
   html_string="<head><style>table {font-family: arial, sans-serif;border-collapse: collapse;width: 100%;}th{text-align: center;border: 1px solid #dddddd;height: 50px;}td{border: 2px solid #dddddd;text-align: left;}tr:nth-child(even) {background-color: #dddddd;}</style></head><body><div style='float:left'><table><tr><th></th><th width=120px>Data</th><th>Photo</th></tr><tr><td> Space ID</td><td> {{space}}</td><td rowspan=\"8\"><img src=\"/static/img/westRemote_6_image.jpg?random={{time}}\"></img></td></tr><tr><td>Authorized</td><td>{{authorized}}</td></tr><tr><td>Student ID</td><td>{{student_ID}}</td></tr><tr><td>First Name</td><td>{{fName}}</td></tr><tr><td>Last Name</td><td>{{lName}}</td></tr><tr><td>License Plate</td><td>{{licPlate}}</td></tr><tr><td>Permission Level</td><td>{{student_perm}}</td></tr><tr><td>Permit Code</td><td>Student Permit</td></tr></table></div></body>"
   html_tail = "</html>"
   f=open("bookshelf/templates/westRemote_6.html","w")
   f.write(html_head+html_string+html_tail)
   f.close()
   return render_template("westRemote_6.html",space=space,authorized=authorized,student_ID=student_ID,fName=fName,lName=lName,licPlate=licPlate,student_perm=student_perm,code=code,time=datetime.now())
@actions.route("westRemote/change0006A")
def westRemotechange0006A():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(6,u'A',westRemote)
   return redirect("westRemote")
@actions.route("westRemote/change0006B")
def westRemotechange0006B():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(6,u'B',westRemote)
   return redirect("westRemote")
@actions.route("westRemote/change0006C")
def westRemotechange0006C():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(6,u'C',westRemote)
   return redirect("westRemote")
@actions.route("westRemote/change0006R")
def westRemotechange0006R():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(6,u'R',westRemote)
   return redirect("westRemote")
@actions.route("eastRemote/claimSpot0006")
def eastRemoteclaimSpot0006():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   claim_space(6,eastRemote)
   return redirect("eastRemote")
@actions.route("eastRemote/free0006")
def eastRemotefree0006():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   free_space(6,eastRemote)
   return redirect("eastRemote")
@actions.route("eastRemote/reserve0006")
def eastRemotereserve0006():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   reserve_space(6,eastRemote)
   return redirect("eastRemote")
@actions.route("eastRemote/view0006")
def eastRemoteview0006():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   space,authorized,student_ID,fName,lName,licPlate,student_perm,code=read_space(eastRemote,6)
   print space,authorized,student_ID,fName,lName,student_perm
   download_blob("images-uploadviagateway","eastRemote_6_image.jpg","bookshelf/static/img/eastRemote_6_image.jpg")
   html_head="<html>"
   html_string="<head><style>table {font-family: arial, sans-serif;border-collapse: collapse;width: 100%;}th{text-align: center;border: 1px solid #dddddd;height: 50px;}td{border: 2px solid #dddddd;text-align: left;}tr:nth-child(even) {background-color: #dddddd;}</style></head><body><div style='float:left'><table><tr><th></th><th width=120px>Data</th><th>Photo</th></tr><tr><td> Space ID</td><td> {{space}}</td><td rowspan=\"8\"><img src=\"/static/img/eastRemote_6_image.jpg?random={{time}}\"></img></td></tr><tr><td>Authorized</td><td>{{authorized}}</td></tr><tr><td>Student ID</td><td>{{student_ID}}</td></tr><tr><td>First Name</td><td>{{fName}}</td></tr><tr><td>Last Name</td><td>{{lName}}</td></tr><tr><td>License Plate</td><td>{{licPlate}}</td></tr><tr><td>Permission Level</td><td>{{student_perm}}</td></tr><tr><td>Permit Code</td><td>Student Permit</td></tr></table></div></body>"
   html_tail = "</html>"
   f=open("bookshelf/templates/eastRemote_6.html","w")
   f.write(html_head+html_string+html_tail)
   f.close()
   return render_template("eastRemote_6.html",space=space,authorized=authorized,student_ID=student_ID,fName=fName,lName=lName,licPlate=licPlate,student_perm=student_perm,code=code,time=datetime.now())
@actions.route("eastRemote/change0006A")
def eastRemotechange0006A():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(6,u'A',eastRemote)
   return redirect("eastRemote")
@actions.route("eastRemote/change0006B")
def eastRemotechange0006B():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(6,u'B',eastRemote)
   return redirect("eastRemote")
@actions.route("eastRemote/change0006C")
def eastRemotechange0006C():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(6,u'C',eastRemote)
   return redirect("eastRemote")
@actions.route("eastRemote/change0006R")
def eastRemotechange0006R():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(6,u'R',eastRemote)
   return redirect("eastRemote")
@actions.route("northRemote/claimSpot0006")
def northRemoteclaimSpot0006():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   claim_space(6,northRemote)
   return redirect("northRemote")
@actions.route("northRemote/free0006")
def northRemotefree0006():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   free_space(6,northRemote)
   return redirect("northRemote")
@actions.route("northRemote/reserve0006")
def northRemotereserve0006():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   reserve_space(6,northRemote)
   return redirect("northRemote")
@actions.route("northRemote/view0006")
def northRemoteview0006():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   space,authorized,student_ID,fName,lName,licPlate,student_perm,code=read_space(northRemote,6)
   print space,authorized,student_ID,fName,lName,student_perm
   download_blob("images-uploadviagateway","northRemote_6_image.jpg","bookshelf/static/img/northRemote_6_image.jpg")
   html_head="<html>"
   html_string="<head><style>table {font-family: arial, sans-serif;border-collapse: collapse;width: 100%;}th{text-align: center;border: 1px solid #dddddd;height: 50px;}td{border: 2px solid #dddddd;text-align: left;}tr:nth-child(even) {background-color: #dddddd;}</style></head><body><div style='float:left'><table><tr><th></th><th width=120px>Data</th><th>Photo</th></tr><tr><td> Space ID</td><td> {{space}}</td><td rowspan=\"8\"><img src=\"/static/img/northRemote_6_image.jpg?random={{time}}\"></img></td></tr><tr><td>Authorized</td><td>{{authorized}}</td></tr><tr><td>Student ID</td><td>{{student_ID}}</td></tr><tr><td>First Name</td><td>{{fName}}</td></tr><tr><td>Last Name</td><td>{{lName}}</td></tr><tr><td>License Plate</td><td>{{licPlate}}</td></tr><tr><td>Permission Level</td><td>{{student_perm}}</td></tr><tr><td>Permit Code</td><td>Student Permit</td></tr></table></div></body>"
   html_tail = "</html>"
   f=open("bookshelf/templates/northRemote_6.html","w")
   f.write(html_head+html_string+html_tail)
   f.close()
   return render_template("northRemote_6.html",space=space,authorized=authorized,student_ID=student_ID,fName=fName,lName=lName,licPlate=licPlate,student_perm=student_perm,code=code,time=datetime.now())
@actions.route("northRemote/change0006A")
def northRemotechange0006A():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(6,u'A',northRemote)
   return redirect("northRemote")
@actions.route("northRemote/change0006B")
def northRemotechange0006B():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(6,u'B',northRemote)
   return redirect("northRemote")
@actions.route("northRemote/change0006C")
def northRemotechange0006C():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(6,u'C',northRemote)
   return redirect("northRemote")
@actions.route("northRemote/change0006R")
def northRemotechange0006R():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(6,u'R',northRemote)
   return redirect("northRemote")
@actions.route("westRemote/claimSpot0007")
def westRemoteclaimSpot0007():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   claim_space(7,westRemote)
   return redirect("westRemote")
@actions.route("westRemote/free0007")
def westRemotefree0007():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   free_space(7,westRemote)
   return redirect("westRemote")
@actions.route("westRemote/reserve0007")
def westRemotereserve0007():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   reserve_space(7,westRemote)
   return redirect("westRemote")
@actions.route("westRemote/view0007")
def westRemoteview0007():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   space,authorized,student_ID,fName,lName,licPlate,student_perm,code=read_space(westRemote,7)
   print space,authorized,student_ID,fName,lName,student_perm
   download_blob("images-uploadviagateway","westRemote_7_image.jpg","bookshelf/static/img/westRemote_7_image.jpg")
   html_head="<html>"
   html_string="<head><style>table {font-family: arial, sans-serif;border-collapse: collapse;width: 100%;}th{text-align: center;border: 1px solid #dddddd;height: 50px;}td{border: 2px solid #dddddd;text-align: left;}tr:nth-child(even) {background-color: #dddddd;}</style></head><body><div style='float:left'><table><tr><th></th><th width=120px>Data</th><th>Photo</th></tr><tr><td> Space ID</td><td> {{space}}</td><td rowspan=\"8\"><img src=\"/static/img/westRemote_7_image.jpg?random={{time}}\"></img></td></tr><tr><td>Authorized</td><td>{{authorized}}</td></tr><tr><td>Student ID</td><td>{{student_ID}}</td></tr><tr><td>First Name</td><td>{{fName}}</td></tr><tr><td>Last Name</td><td>{{lName}}</td></tr><tr><td>License Plate</td><td>{{licPlate}}</td></tr><tr><td>Permission Level</td><td>{{student_perm}}</td></tr><tr><td>Permit Code</td><td>Student Permit</td></tr></table></div></body>"
   html_tail = "</html>"
   f=open("bookshelf/templates/westRemote_7.html","w")
   f.write(html_head+html_string+html_tail)
   f.close()
   return render_template("westRemote_7.html",space=space,authorized=authorized,student_ID=student_ID,fName=fName,lName=lName,licPlate=licPlate,student_perm=student_perm,code=code,time=datetime.now())
@actions.route("westRemote/change0007A")
def westRemotechange0007A():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(7,u'A',westRemote)
   return redirect("westRemote")
@actions.route("westRemote/change0007B")
def westRemotechange0007B():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(7,u'B',westRemote)
   return redirect("westRemote")
@actions.route("westRemote/change0007C")
def westRemotechange0007C():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(7,u'C',westRemote)
   return redirect("westRemote")
@actions.route("westRemote/change0007R")
def westRemotechange0007R():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(7,u'R',westRemote)
   return redirect("westRemote")
@actions.route("eastRemote/claimSpot0007")
def eastRemoteclaimSpot0007():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   claim_space(7,eastRemote)
   return redirect("eastRemote")
@actions.route("eastRemote/free0007")
def eastRemotefree0007():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   free_space(7,eastRemote)
   return redirect("eastRemote")
@actions.route("eastRemote/reserve0007")
def eastRemotereserve0007():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   reserve_space(7,eastRemote)
   return redirect("eastRemote")
@actions.route("eastRemote/view0007")
def eastRemoteview0007():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   space,authorized,student_ID,fName,lName,licPlate,student_perm,code=read_space(eastRemote,7)
   print space,authorized,student_ID,fName,lName,student_perm
   download_blob("images-uploadviagateway","eastRemote_7_image.jpg","bookshelf/static/img/eastRemote_7_image.jpg")
   html_head="<html>"
   html_string="<head><style>table {font-family: arial, sans-serif;border-collapse: collapse;width: 100%;}th{text-align: center;border: 1px solid #dddddd;height: 50px;}td{border: 2px solid #dddddd;text-align: left;}tr:nth-child(even) {background-color: #dddddd;}</style></head><body><div style='float:left'><table><tr><th></th><th width=120px>Data</th><th>Photo</th></tr><tr><td> Space ID</td><td> {{space}}</td><td rowspan=\"8\"><img src=\"/static/img/eastRemote_7_image.jpg?random={{time}}\"></img></td></tr><tr><td>Authorized</td><td>{{authorized}}</td></tr><tr><td>Student ID</td><td>{{student_ID}}</td></tr><tr><td>First Name</td><td>{{fName}}</td></tr><tr><td>Last Name</td><td>{{lName}}</td></tr><tr><td>License Plate</td><td>{{licPlate}}</td></tr><tr><td>Permission Level</td><td>{{student_perm}}</td></tr><tr><td>Permit Code</td><td>Student Permit</td></tr></table></div></body>"
   html_tail = "</html>"
   f=open("bookshelf/templates/eastRemote_7.html","w")
   f.write(html_head+html_string+html_tail)
   f.close()
   return render_template("eastRemote_7.html",space=space,authorized=authorized,student_ID=student_ID,fName=fName,lName=lName,licPlate=licPlate,student_perm=student_perm,code=code,time=datetime.now())
@actions.route("eastRemote/change0007A")
def eastRemotechange0007A():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(7,u'A',eastRemote)
   return redirect("eastRemote")
@actions.route("eastRemote/change0007B")
def eastRemotechange0007B():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(7,u'B',eastRemote)
   return redirect("eastRemote")
@actions.route("eastRemote/change0007C")
def eastRemotechange0007C():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(7,u'C',eastRemote)
   return redirect("eastRemote")
@actions.route("eastRemote/change0007R")
def eastRemotechange0007R():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(7,u'R',eastRemote)
   return redirect("eastRemote")
@actions.route("northRemote/claimSpot0007")
def northRemoteclaimSpot0007():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   claim_space(7,northRemote)
   return redirect("northRemote")
@actions.route("northRemote/free0007")
def northRemotefree0007():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   free_space(7,northRemote)
   return redirect("northRemote")
@actions.route("northRemote/reserve0007")
def northRemotereserve0007():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   reserve_space(7,northRemote)
   return redirect("northRemote")
@actions.route("northRemote/view0007")
def northRemoteview0007():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   space,authorized,student_ID,fName,lName,licPlate,student_perm,code=read_space(northRemote,7)
   print space,authorized,student_ID,fName,lName,student_perm
   download_blob("images-uploadviagateway","northRemote_7_image.jpg","bookshelf/static/img/northRemote_7_image.jpg")
   html_head="<html>"
   html_string="<head><style>table {font-family: arial, sans-serif;border-collapse: collapse;width: 100%;}th{text-align: center;border: 1px solid #dddddd;height: 50px;}td{border: 2px solid #dddddd;text-align: left;}tr:nth-child(even) {background-color: #dddddd;}</style></head><body><div style='float:left'><table><tr><th></th><th width=120px>Data</th><th>Photo</th></tr><tr><td> Space ID</td><td> {{space}}</td><td rowspan=\"8\"><img src=\"/static/img/northRemote_7_image.jpg?random={{time}}\"></img></td></tr><tr><td>Authorized</td><td>{{authorized}}</td></tr><tr><td>Student ID</td><td>{{student_ID}}</td></tr><tr><td>First Name</td><td>{{fName}}</td></tr><tr><td>Last Name</td><td>{{lName}}</td></tr><tr><td>License Plate</td><td>{{licPlate}}</td></tr><tr><td>Permission Level</td><td>{{student_perm}}</td></tr><tr><td>Permit Code</td><td>Student Permit</td></tr></table></div></body>"
   html_tail = "</html>"
   f=open("bookshelf/templates/northRemote_7.html","w")
   f.write(html_head+html_string+html_tail)
   f.close()
   return render_template("northRemote_7.html",space=space,authorized=authorized,student_ID=student_ID,fName=fName,lName=lName,licPlate=licPlate,student_perm=student_perm,code=code,time=datetime.now())
@actions.route("northRemote/change0007A")
def northRemotechange0007A():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(7,u'A',northRemote)
   return redirect("northRemote")
@actions.route("northRemote/change0007B")
def northRemotechange0007B():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(7,u'B',northRemote)
   return redirect("northRemote")
@actions.route("northRemote/change0007C")
def northRemotechange0007C():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(7,u'C',northRemote)
   return redirect("northRemote")
@actions.route("northRemote/change0007R")
def northRemotechange0007R():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(7,u'R',northRemote)
   return redirect("northRemote")
@actions.route("westRemote/claimSpot0008")
def westRemoteclaimSpot0008():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   claim_space(8,westRemote)
   return redirect("westRemote")
@actions.route("westRemote/free0008")
def westRemotefree0008():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   free_space(8,westRemote)
   return redirect("westRemote")
@actions.route("westRemote/reserve0008")
def westRemotereserve0008():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   reserve_space(8,westRemote)
   return redirect("westRemote")
@actions.route("westRemote/view0008")
def westRemoteview0008():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   space,authorized,student_ID,fName,lName,licPlate,student_perm,code=read_space(westRemote,8)
   print space,authorized,student_ID,fName,lName,student_perm
   download_blob("images-uploadviagateway","westRemote_8_image.jpg","bookshelf/static/img/westRemote_8_image.jpg")
   html_head="<html>"
   html_string="<head><style>table {font-family: arial, sans-serif;border-collapse: collapse;width: 100%;}th{text-align: center;border: 1px solid #dddddd;height: 50px;}td{border: 2px solid #dddddd;text-align: left;}tr:nth-child(even) {background-color: #dddddd;}</style></head><body><div style='float:left'><table><tr><th></th><th width=120px>Data</th><th>Photo</th></tr><tr><td> Space ID</td><td> {{space}}</td><td rowspan=\"8\"><img src=\"/static/img/westRemote_8_image.jpg?random={{time}}\"></img></td></tr><tr><td>Authorized</td><td>{{authorized}}</td></tr><tr><td>Student ID</td><td>{{student_ID}}</td></tr><tr><td>First Name</td><td>{{fName}}</td></tr><tr><td>Last Name</td><td>{{lName}}</td></tr><tr><td>License Plate</td><td>{{licPlate}}</td></tr><tr><td>Permission Level</td><td>{{student_perm}}</td></tr><tr><td>Permit Code</td><td>Student Permit</td></tr></table></div></body>"
   html_tail = "</html>"
   f=open("bookshelf/templates/westRemote_8.html","w")
   f.write(html_head+html_string+html_tail)
   f.close()
   return render_template("westRemote_8.html",space=space,authorized=authorized,student_ID=student_ID,fName=fName,lName=lName,licPlate=licPlate,student_perm=student_perm,code=code,time=datetime.now())
@actions.route("westRemote/change0008A")
def westRemotechange0008A():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(8,u'A',westRemote)
   return redirect("westRemote")
@actions.route("westRemote/change0008B")
def westRemotechange0008B():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(8,u'B',westRemote)
   return redirect("westRemote")
@actions.route("westRemote/change0008C")
def westRemotechange0008C():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(8,u'C',westRemote)
   return redirect("westRemote")
@actions.route("westRemote/change0008R")
def westRemotechange0008R():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(8,u'R',westRemote)
   return redirect("westRemote")
@actions.route("eastRemote/claimSpot0008")
def eastRemoteclaimSpot0008():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   claim_space(8,eastRemote)
   return redirect("eastRemote")
@actions.route("eastRemote/free0008")
def eastRemotefree0008():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   free_space(8,eastRemote)
   return redirect("eastRemote")
@actions.route("eastRemote/reserve0008")
def eastRemotereserve0008():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   reserve_space(8,eastRemote)
   return redirect("eastRemote")
@actions.route("eastRemote/view0008")
def eastRemoteview0008():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   space,authorized,student_ID,fName,lName,licPlate,student_perm,code=read_space(eastRemote,8)
   print space,authorized,student_ID,fName,lName,student_perm
   download_blob("images-uploadviagateway","eastRemote_8_image.jpg","bookshelf/static/img/eastRemote_8_image.jpg")
   html_head="<html>"
   html_string="<head><style>table {font-family: arial, sans-serif;border-collapse: collapse;width: 100%;}th{text-align: center;border: 1px solid #dddddd;height: 50px;}td{border: 2px solid #dddddd;text-align: left;}tr:nth-child(even) {background-color: #dddddd;}</style></head><body><div style='float:left'><table><tr><th></th><th width=120px>Data</th><th>Photo</th></tr><tr><td> Space ID</td><td> {{space}}</td><td rowspan=\"8\"><img src=\"/static/img/eastRemote_8_image.jpg?random={{time}}\"></img></td></tr><tr><td>Authorized</td><td>{{authorized}}</td></tr><tr><td>Student ID</td><td>{{student_ID}}</td></tr><tr><td>First Name</td><td>{{fName}}</td></tr><tr><td>Last Name</td><td>{{lName}}</td></tr><tr><td>License Plate</td><td>{{licPlate}}</td></tr><tr><td>Permission Level</td><td>{{student_perm}}</td></tr><tr><td>Permit Code</td><td>Student Permit</td></tr></table></div></body>"
   html_tail = "</html>"
   f=open("bookshelf/templates/eastRemote_8.html","w")
   f.write(html_head+html_string+html_tail)
   f.close()
   return render_template("eastRemote_8.html",space=space,authorized=authorized,student_ID=student_ID,fName=fName,lName=lName,licPlate=licPlate,student_perm=student_perm,code=code,time=datetime.now())
@actions.route("eastRemote/change0008A")
def eastRemotechange0008A():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(8,u'A',eastRemote)
   return redirect("eastRemote")
@actions.route("eastRemote/change0008B")
def eastRemotechange0008B():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(8,u'B',eastRemote)
   return redirect("eastRemote")
@actions.route("eastRemote/change0008C")
def eastRemotechange0008C():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(8,u'C',eastRemote)
   return redirect("eastRemote")
@actions.route("eastRemote/change0008R")
def eastRemotechange0008R():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(8,u'R',eastRemote)
   return redirect("eastRemote")
@actions.route("northRemote/claimSpot0008")
def northRemoteclaimSpot0008():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   claim_space(8,northRemote)
   return redirect("northRemote")
@actions.route("northRemote/free0008")
def northRemotefree0008():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   free_space(8,northRemote)
   return redirect("northRemote")
@actions.route("northRemote/reserve0008")
def northRemotereserve0008():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   reserve_space(8,northRemote)
   return redirect("northRemote")
@actions.route("northRemote/view0008")
def northRemoteview0008():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   space,authorized,student_ID,fName,lName,licPlate,student_perm,code=read_space(northRemote,8)
   print space,authorized,student_ID,fName,lName,student_perm
   download_blob("images-uploadviagateway","northRemote_8_image.jpg","bookshelf/static/img/northRemote_8_image.jpg")
   html_head="<html>"
   html_string="<head><style>table {font-family: arial, sans-serif;border-collapse: collapse;width: 100%;}th{text-align: center;border: 1px solid #dddddd;height: 50px;}td{border: 2px solid #dddddd;text-align: left;}tr:nth-child(even) {background-color: #dddddd;}</style></head><body><div style='float:left'><table><tr><th></th><th width=120px>Data</th><th>Photo</th></tr><tr><td> Space ID</td><td> {{space}}</td><td rowspan=\"8\"><img src=\"/static/img/northRemote_8_image.jpg?random={{time}}\"></img></td></tr><tr><td>Authorized</td><td>{{authorized}}</td></tr><tr><td>Student ID</td><td>{{student_ID}}</td></tr><tr><td>First Name</td><td>{{fName}}</td></tr><tr><td>Last Name</td><td>{{lName}}</td></tr><tr><td>License Plate</td><td>{{licPlate}}</td></tr><tr><td>Permission Level</td><td>{{student_perm}}</td></tr><tr><td>Permit Code</td><td>Student Permit</td></tr></table></div></body>"
   html_tail = "</html>"
   f=open("bookshelf/templates/northRemote_8.html","w")
   f.write(html_head+html_string+html_tail)
   f.close()
   return render_template("northRemote_8.html",space=space,authorized=authorized,student_ID=student_ID,fName=fName,lName=lName,licPlate=licPlate,student_perm=student_perm,code=code,time=datetime.now())
@actions.route("northRemote/change0008A")
def northRemotechange0008A():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(8,u'A',northRemote)
   return redirect("northRemote")
@actions.route("northRemote/change0008B")
def northRemotechange0008B():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(8,u'B',northRemote)
   return redirect("northRemote")
@actions.route("northRemote/change0008C")
def northRemotechange0008C():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(8,u'C',northRemote)
   return redirect("northRemote")
@actions.route("northRemote/change0008R")
def northRemotechange0008R():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(8,u'R',northRemote)
   return redirect("northRemote")
@actions.route("westRemote/claimSpot0009")
def westRemoteclaimSpot0009():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   claim_space(9,westRemote)
   return redirect("westRemote")
@actions.route("westRemote/free0009")
def westRemotefree0009():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   free_space(9,westRemote)
   return redirect("westRemote")
@actions.route("westRemote/reserve0009")
def westRemotereserve0009():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   reserve_space(9,westRemote)
   return redirect("westRemote")
@actions.route("westRemote/view0009")
def westRemoteview0009():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   space,authorized,student_ID,fName,lName,licPlate,student_perm,code=read_space(westRemote,9)
   print space,authorized,student_ID,fName,lName,student_perm
   download_blob("images-uploadviagateway","westRemote_9_image.jpg","bookshelf/static/img/westRemote_9_image.jpg")
   html_head="<html>"
   html_string="<head><style>table {font-family: arial, sans-serif;border-collapse: collapse;width: 100%;}th{text-align: center;border: 1px solid #dddddd;height: 50px;}td{border: 2px solid #dddddd;text-align: left;}tr:nth-child(even) {background-color: #dddddd;}</style></head><body><div style='float:left'><table><tr><th></th><th width=120px>Data</th><th>Photo</th></tr><tr><td> Space ID</td><td> {{space}}</td><td rowspan=\"8\"><img src=\"/static/img/westRemote_9_image.jpg?random={{time}}\"></img></td></tr><tr><td>Authorized</td><td>{{authorized}}</td></tr><tr><td>Student ID</td><td>{{student_ID}}</td></tr><tr><td>First Name</td><td>{{fName}}</td></tr><tr><td>Last Name</td><td>{{lName}}</td></tr><tr><td>License Plate</td><td>{{licPlate}}</td></tr><tr><td>Permission Level</td><td>{{student_perm}}</td></tr><tr><td>Permit Code</td><td>Student Permit</td></tr></table></div></body>"
   html_tail = "</html>"
   f=open("bookshelf/templates/westRemote_9.html","w")
   f.write(html_head+html_string+html_tail)
   f.close()
   return render_template("westRemote_9.html",space=space,authorized=authorized,student_ID=student_ID,fName=fName,lName=lName,licPlate=licPlate,student_perm=student_perm,code=code,time=datetime.now())
@actions.route("westRemote/change0009A")
def westRemotechange0009A():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(9,u'A',westRemote)
   return redirect("westRemote")
@actions.route("westRemote/change0009B")
def westRemotechange0009B():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(9,u'B',westRemote)
   return redirect("westRemote")
@actions.route("westRemote/change0009C")
def westRemotechange0009C():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(9,u'C',westRemote)
   return redirect("westRemote")
@actions.route("westRemote/change0009R")
def westRemotechange0009R():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(9,u'R',westRemote)
   return redirect("westRemote")
@actions.route("eastRemote/claimSpot0009")
def eastRemoteclaimSpot0009():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   claim_space(9,eastRemote)
   return redirect("eastRemote")
@actions.route("eastRemote/free0009")
def eastRemotefree0009():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   free_space(9,eastRemote)
   return redirect("eastRemote")
@actions.route("eastRemote/reserve0009")
def eastRemotereserve0009():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   reserve_space(9,eastRemote)
   return redirect("eastRemote")
@actions.route("eastRemote/view0009")
def eastRemoteview0009():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   space,authorized,student_ID,fName,lName,licPlate,student_perm,code=read_space(eastRemote,9)
   print space,authorized,student_ID,fName,lName,student_perm
   download_blob("images-uploadviagateway","eastRemote_9_image.jpg","bookshelf/static/img/eastRemote_9_image.jpg")
   html_head="<html>"
   html_string="<head><style>table {font-family: arial, sans-serif;border-collapse: collapse;width: 100%;}th{text-align: center;border: 1px solid #dddddd;height: 50px;}td{border: 2px solid #dddddd;text-align: left;}tr:nth-child(even) {background-color: #dddddd;}</style></head><body><div style='float:left'><table><tr><th></th><th width=120px>Data</th><th>Photo</th></tr><tr><td> Space ID</td><td> {{space}}</td><td rowspan=\"8\"><img src=\"/static/img/eastRemote_9_image.jpg?random={{time}}\"></img></td></tr><tr><td>Authorized</td><td>{{authorized}}</td></tr><tr><td>Student ID</td><td>{{student_ID}}</td></tr><tr><td>First Name</td><td>{{fName}}</td></tr><tr><td>Last Name</td><td>{{lName}}</td></tr><tr><td>License Plate</td><td>{{licPlate}}</td></tr><tr><td>Permission Level</td><td>{{student_perm}}</td></tr><tr><td>Permit Code</td><td>Student Permit</td></tr></table></div></body>"
   html_tail = "</html>"
   f=open("bookshelf/templates/eastRemote_9.html","w")
   f.write(html_head+html_string+html_tail)
   f.close()
   return render_template("eastRemote_9.html",space=space,authorized=authorized,student_ID=student_ID,fName=fName,lName=lName,licPlate=licPlate,student_perm=student_perm,code=code,time=datetime.now())
@actions.route("eastRemote/change0009A")
def eastRemotechange0009A():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(9,u'A',eastRemote)
   return redirect("eastRemote")
@actions.route("eastRemote/change0009B")
def eastRemotechange0009B():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(9,u'B',eastRemote)
   return redirect("eastRemote")
@actions.route("eastRemote/change0009C")
def eastRemotechange0009C():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(9,u'C',eastRemote)
   return redirect("eastRemote")
@actions.route("eastRemote/change0009R")
def eastRemotechange0009R():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(9,u'R',eastRemote)
   return redirect("eastRemote")
@actions.route("northRemote/claimSpot0009")
def northRemoteclaimSpot0009():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   claim_space(9,northRemote)
   return redirect("northRemote")
@actions.route("northRemote/free0009")
def northRemotefree0009():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   free_space(9,northRemote)
   return redirect("northRemote")
@actions.route("northRemote/reserve0009")
def northRemotereserve0009():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   reserve_space(9,northRemote)
   return redirect("northRemote")
@actions.route("northRemote/view0009")
def northRemoteview0009():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   space,authorized,student_ID,fName,lName,licPlate,student_perm,code=read_space(northRemote,9)
   print space,authorized,student_ID,fName,lName,student_perm
   download_blob("images-uploadviagateway","northRemote_9_image.jpg","bookshelf/static/img/northRemote_9_image.jpg")
   html_head="<html>"
   html_string="<head><style>table {font-family: arial, sans-serif;border-collapse: collapse;width: 100%;}th{text-align: center;border: 1px solid #dddddd;height: 50px;}td{border: 2px solid #dddddd;text-align: left;}tr:nth-child(even) {background-color: #dddddd;}</style></head><body><div style='float:left'><table><tr><th></th><th width=120px>Data</th><th>Photo</th></tr><tr><td> Space ID</td><td> {{space}}</td><td rowspan=\"8\"><img src=\"/static/img/northRemote_9_image.jpg?random={{time}}\"></img></td></tr><tr><td>Authorized</td><td>{{authorized}}</td></tr><tr><td>Student ID</td><td>{{student_ID}}</td></tr><tr><td>First Name</td><td>{{fName}}</td></tr><tr><td>Last Name</td><td>{{lName}}</td></tr><tr><td>License Plate</td><td>{{licPlate}}</td></tr><tr><td>Permission Level</td><td>{{student_perm}}</td></tr><tr><td>Permit Code</td><td>Student Permit</td></tr></table></div></body>"
   html_tail = "</html>"
   f=open("bookshelf/templates/northRemote_9.html","w")
   f.write(html_head+html_string+html_tail)
   f.close()
   return render_template("northRemote_9.html",space=space,authorized=authorized,student_ID=student_ID,fName=fName,lName=lName,licPlate=licPlate,student_perm=student_perm,code=code,time=datetime.now())
@actions.route("northRemote/change0009A")
def northRemotechange0009A():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(9,u'A',northRemote)
   return redirect("northRemote")
@actions.route("northRemote/change0009B")
def northRemotechange0009B():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(9,u'B',northRemote)
   return redirect("northRemote")
@actions.route("northRemote/change0009C")
def northRemotechange0009C():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(9,u'C',northRemote)
   return redirect("northRemote")
@actions.route("northRemote/change0009R")
def northRemotechange0009R():
   username = request.cookies.get('username')
   if not username:
      return redirect("/")
   change_space_permission(9,u'R',northRemote)
   return redirect("northRemote")
