import urllib
import time
import sys
import subprocess

print subprocess.call(["cat","/var/lib/misc/dnsmasq.leases"])

link = "http://10.3.141.194"
f = urllib.urlopen(link)
myfile = f.read()

myfilesplit = myfile.split('<br>')
print myfilesplit
print myfile


while(1):
    time.sleep(2)
    f = urllib.urlopen(link)
    myfile = f.read()
    lines = myfile.split('<br>')
    if(len(lines) >= 2):
        if(lines[0] == 'Status_Changed'):
            awk = urllib.urlopen(link + '/ACK')
            print("The parking spot status has changed to " + lines[1] + "\n" + "Sent ACK signal")
        else:
            print("The parking spot status is " + lines[1] + "\n")
    else:
        print("ERROR: size less than 2\n")



