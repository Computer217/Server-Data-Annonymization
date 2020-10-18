#!/usr/bin/python3
import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import random
import string
import csv
import sys
from datetime import datetime
sys.path.append("/etc/neteng/scripts/lib/")
from apiprimereport import getReport
global AIRPORTCODES
global PLACENAMES
global MACHASHDB
global NETIDHASHDB
AIRPORTCODES = './db/airportcodes_2'
PLACENAMES = './db/cities3'
MACHASHDB = './db/mac_hashtable'
NETIDHASHDB = './db/netid_hashtable'
CSVOUTPUT ='./output/'
airportset= set()
cityset = set()
knownmacset = set()
knownnetidset = set()
usedmachashset = set()
usednetidhashset = set()
#Seed data sets
with open(AIRPORTCODES , 'r') as buffer:

    for line in buffer:
        # remove linebreak which is the last character of the string
        airport= line[:-1] 

        # add item to the list
        airportset.add(airport)



with open(PLACENAMES, 'r') as buffer:

	for line in buffer:
	 readcity = line[:-1]
	 cityset.add(readcity)

airportlist = list(airportset)  # raw data used for hashing mac addresses
citylist = list(cityset)	# raw data used from hashing netids

# load assigned MAC/NETID sets
netidhash = {} 
machash = {}
decode_netidhash = {}
decode_machash = {}
with open(NETIDHASHDB, newline='') as buffer:
	
        #each line of NETIDHASHDB is an entry of Hash|NetID seperated by the pipe symbol

        #word file described NETIDHASHDB as NetID|Place name hash

        for line in buffer:
                entry = line[:-1]
                (hash, netid ) = entry.split('|')
                netid=netid.lower()

                netidhash[ netid ] = hash
                decode_netidhash[hash] = netid
                knownnetidset.add(netid)
                usednetidhashset.add(hash)


with open(MACHASHDB , 'r') as buffer:

        for line in buffer:
                entry = line[:-1]
                (hash, mac ) = entry.split('|')
                mac = mac.lower()
                machash[ mac ] = hash
                decode_machash[ hash ] = mac
                knownmacset.add(mac)
                usedmachashset.add(hash)

# define functions here
def openhashdb(type):
        if type == 'netid':
                fh = open(NETIDHASHDB , 'a')




        elif type == 'mac':

                fh = open(MACHASHDB , 'a')

        else:
                return False

        return fh



def makehash(data , type):
	print("In function")
	wordlist=list()
	if data:
		print(type)
		if (type == "netid") or (type == "mac"):

                        fh = openhashdb(type)


                        if type == 'mac':
                                print("MAC")
                                wordlist = getHashseed("mac")
                                maclist=list(data)   
                                while maclist:
                                        random.shuffle(maclist)
                                        random.shuffle(wordlist)
                                        while 1:
                                                hash1 = random.choice(wordlist)
                                                hash2 = random.choice(wordlist)
                                                hash3 = random.choice(wordlist)
                                                hash4 = random.choice(wordlist)
                                                hash5 = random.choice(wordlist)
                                                hash6 = random.choice(wordlist)
                                                hash = hash1 + ":" + hash2 + ":" + hash3 + ":" + hash4 + ":" + hash5 + ":" + hash6
                                                hash = hash.lower()
                                                if hash not in usedmachashset:
                                                        maskmac = (random.choice(maclist))
                                                        machash[maskmac] = hash
                                                        decode_machash[hash] = maskmac
                                                        knownmacset.add(maskmac)
                                                        usedmachashset.add(hash)
                                                        
                                                        fh.write(hash + "|" + maskmac + "\n")

                                                        maclist.remove(maskmac)
                                                        
                                                        break
                                                else:
                                                        print("NON-UNIQUE HASH FOUND RECALC")
                                        random.shuffle(maclist)
                        elif type == 'netid':

                                wordlist = getHashseed("netid")
                                netidlist=list(data)
                                while netidlist:
                                        random.shuffle(netidlist)
                                        random.shuffle(wordlist)
                                        while 1:
                                                        hash1 = random.choice(wordlist)
                                                        hash2 = random.choice(wordlist)
                                                        hash3 = random.choice(wordlist)
                                                        hash4 = random.choice(wordlist)
                                                        hash5 = random.choice(wordlist)
                                                        hash6 = random.choice(wordlist)
                                                        hash = hash1 + ":" + hash2 + ":" + hash3 + ":" + hash4 + ":" + hash5 + ":" + hash6
                                                        hash = hash.lower()
                                                        if hash not in usednetidhashset:
                                                                masknetid = (random.choice(netidlist))
                                                                netidhash[masknetid] = hash
                                                                decode_netidhash[hash] = masknetid
                                                                knownnetidset.add(masknetid)
                                                                usednetidhashset.add(hash)
                                                                fh.write(hash+ "|" + masknetid+"\n")
                                                                netidlist.remove(masknetid)
                                                                break
                                                        else:
                                                                print("NON-UNIQUE HASH FOUND RECALC")
                                                        random.shuffle(netidlist)


                        else:
                                return false

	else:

                return false


	fh.close()

def getHashseed(type):
        wordset=set()
        if type == 'mac':

                with open(AIRPORTCODES , 'r') as buffer:

                        for line in buffer:
                        # remove linebreak which is the last character of the string
                                wordentry = line[:-1]

                        # add item to the list
                                wordset.add(wordentry)
                return list(wordset)

        elif type == 'netid':

                with open(PLACENAMES, 'r') as buffer:

                        for line in buffer:
                        # remove linebreak which is the last character of the string
                                wordentry = line[:-1]

                        # add item to the list
                                wordset.add(wordentry)
                return list(wordset)
        else:

                return False



#get report Json and pull unknown netids and mac addresses


report = getReport("reportname" , "json")
if report == 'ERROR':

	exit()


reportnetids = set()
reportmacs = set()
macs2bhashed=set()
netids2bhashed=set()
for row in report:

#Client Username
#Client MAC Address
#SSID
        #get Mac from Report 
	rowmac=report[row]['Client MAC Address'].lower()
	reportmacs.add(rowmac)
        #get netID from Report
	if report[row][ 'SSID' ] == "UCONN-SECURE" or report[row][ 'SSID' ] == "EDUROAM":
		rownetid=report[row]['Client Username'].lower()
		reportnetids.add(rownetid)
			

# compare to known netid/mac to determine if new hashes need to be generated
	reportmacs.add("testfoo")
	reportmacs.add("testfoo2")
	reportnetids.add("testnetidfoo")
	reportnetids.add("testnetidfoo2")
	macs2bhashed = reportmacs.difference(knownmacset)
	
	netids2bhashed = reportnetids.difference(knownnetidset)



if macs2bhashed:
	makehash(macs2bhashed, "mac")

if netids2bhashed:

	makehash(netids2bhashed, "netid")



timestamp=int(datetime.timestamp(datetime.now()))
outputfile = open(CSVOUTPUT + "wifi_anon_" + str(timestamp)+".csv", 'w')
filetosend=CSVOUTPUT + "wifi_anon_" + str(timestamp) + ".csv"
csvwriter = csv.DictWriter(outputfile, report[row].keys())
headerwritten=bool(0)
for row in report:

	rowmac=report[row]['Client MAC Address'].lower()
	report[row]['Client MAC Address'] = machash[rowmac]
	if report[row][ 'SSID' ] == "UCONN-SECURE" or report[row][ 'SSID' ] == "EDUROAM":
                rownetid=report[row]['Client Username'].lower()
                report[row]['Client Username'] = netidhash[rownetid]

	if not headerwritten:
		csvwriter.writeheader()
		headerwritten = bool(1)
	csvwriter.writerow(report[row])



msg = MIMEMultipart()
fromaddr ='sender@uconn.edu'
msg['From'] = fromaddr
msg["To"] = "sender@uconn.edu"
msg['Subject'] = "Report"

htmlEmail = """
<p>    Please find the attached Report below.<br/><br/>
<br/></p>
"""
fp = open(filetosend)
ctype, encoding = mimetypes.guess_type(filetosend)
if ctype is None or encoding is not None:
    ctype = "application/octet-stream"

maintype, subtype = ctype.split("/", 1)

attachment = MIMEText(fp.read(), _subtype=subtype)
fp.close()
attachment.add_header("Content-Disposition", "attachment", filename=filetosend)
msg.attach(attachment)

server = smtplib.SMTP('smtp.uconn.edu', 25)
server.starttls()
text = msg.as_string()
server.sendmail('sender@uconn.edu' ,['recipient@uconn.edu','recipient@uconn.edu'], text)
server.quit()


#Script Maintenance 
path = '/etc/neteng/scripts/output'


for filename in os.listdir(path):
        #if csv file is older than 7 days 
        file_unix_time = filename.split("_")[2]

        try:
                result = timestamp - file_unix_time > 604800
        except:
                if file_unix_time[10:] == ".csv":
                        file_unix_time = int(file_unix_time[:10])

                else:
                        print("file format error in clean up script => not .csv")

        if filename.endswith(".csv") and (timestamp - file_unix_time > 604800):
                os.remove(path + "/" + str(filename))        
        else:
                continue 

#Script Maintenance


