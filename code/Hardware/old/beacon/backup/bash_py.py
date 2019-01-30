import sys
import subprocess
DEBUG = False #print extra debug info

url = "" #for debugging, returns the extact url from the setup file

def setupToHex ( ):
    filename = "setup.txt" #opens the setup file
    file = open(filename, "r") #sets the file to read
    print "Opened setup.txt"
    print "Creating URL"
    for line in file: #read each line of the file
        line = line.rstrip('\n') #strip the return char
        a, b = line.split('=')
        if(a == 'HEADER'):
            url = b
            if DEBUG: print "Found Header: " + b 
            
            if(b == 'http://www.'):
                HEADER = ' 00'
            elif(b == 'https://www.'):
                HEADER = ' 01'
            elif(b == 'http://'):
                HEADER = ' 02'
            elif(b == 'https://'):
                HEADER = ' 03'
            else:
                print "ERROR: Invalid header"
            if DEBUG: print "HEX: " + HEADER + "\n"

        elif(a == 'URL'):
            url = url + b
            if DEBUG: print "Found URL:    " + b
            
            URL = ""
            for letter in b:
                URL =  URL + ' ' + letter.encode("hex")
            if DEBUG: print "HEX: " + URL + "\n"

        elif(a == 'TLD'):
            url = url + b
            if DEBUG: print "Found TLD:    " + b
            
            if  (b == '.com/'):
                TLD = ' 00'
            elif(b == '.org/'):
                TLD = ' 01'
            elif(b == '.edu/'):
                TLD = ' 02'
            elif(b == '.net/'):
                TLD = ' 03'
            elif(b == '.info/'):
                TLD = ' 04'
            elif(b == '.biz/'):
                TLD = ' 05'
            elif(b == '.gov/'):
                TLD = ' 06'
            elif(b == '.com'):
                TLD = ' 07'
            elif(b == '.org'):
                TLD = ' 08'
            elif(b == '.edu'):
                TLD = ' 09'
            elif(b == '.net'):
                TLD = ' 0a'
            elif(b == '.info'):
                TLD = ' 0b'
            elif(b == '.biz'):
                TLD = ' 0c'
            elif(b == '.gov'):
                TLD = ' 0d'

            else:
                print "ERROR: TLD"           
            if DEBUG: print "HEX: " + TLD + "\n"
        elif(a == 'LOT'):
            url = url + b
            if DEBUG: print "Found LOT:    " + b
            
            LOT = ""
            for letter in b:
                LOT = LOT + ' ' + letter.encode("hex")
            if DEBUG: print "HEX: " + LOT + "\n"

        elif(a == 'BLOCK'):
            url = url + '/' + b
            if DEBUG: print "Found BLOCK:  " + b

            BLOCK = ' 2f'
            for letter in b:
                BLOCK = BLOCK + ' ' + letter.encode("hex")
            if DEBUG: print "HEX: " + BLOCK + "\n"

        elif(a == 'SPOT'):
            url = url + '/' + b
            if DEBUG: print "Found SPOT:   " + b
            
            SPOT = ' 2f'
            for letter in b:
                SPOT = SPOT + ' ' + letter.encode("hex")
            if DEBUG: print "HEX: " + SPOT + "\n"

        else:
            print "ERROR: invalid param"
    
    file.close()
    
    print "Attempting to make the following URL: " + url 

    frame = HEADER + URL + TLD + LOT + BLOCK + SPOT
    frame_noSpace = frame.replace(" ", "")
    frame_length = len(frame_noSpace)/2
    if DEBUG: print "frame_lenth: " + '{:02x}'.format(frame_length) # hex(frame_length)

    length1 = frame_length + 13
    length2 = frame_length + 5
    
    if((18 - frame_length) < 0):
        print "ERROR: Frame length to large. Reduce by " + \
                str(frame_length - 18) + " char."
        print "Failed to create beacon.sh"
        succ = 0
    else:
        f = open("beacon.sh", "w")
        f.writelines('#!/bin/bash' + "\n")
        f.writelines("sudo hciconfig hci0 up\n")
        f.writelines("sudo hciconfig hci0 leadv 3\n")
    

        zeros = ""
        for i in range(0, 18 - frame_length):
            zeros  =  zeros + ' 00'

        f.writelines("sudo hcitool -i hci0 cmd 0x08 0x0008 " + \
                '{:02x}'.format(length1) + \
                " 02 01 06 03 03 aa fe " + \
                '{:02x}'.format(length2) + \
                ' 16 aa fe 10 00' + \
                HEADER + URL + TLD + LOT + BLOCK + SPOT + \
                zeros)

        f.close()
        print "Created: Beacon.sh\n\n"
        succ = 1
        if DEBUG: print HEADER + URL + TLD + LOT + BLOCK + SPOT
    
    return url, succ

def runBeacon():
    subprocess.call(["chmod", '+x', 'beacon.sh'])
    print "--- START OF beacon.sh ---"
    subprocess.call(["cat", "beacon.sh"])
    print "\n--- END OF beacon ---\n"
    print "Starting the beacon: "
    subprocess.call(["sudo", './beacon.sh'])
    print "\nBeacon has been started and points to the following URL: " + url

url, succ = setupToHex()
if(succ and (sys.argv[1] == 'run')):
    runBeacon()

print "\n"
