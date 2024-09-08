import requests
import json
import sys
sys.path.append("/etc/neteng/scripts/lib/")
from XGLOBALS import *
PRIMEGETREPORTURLSTRING = "v4/op/reportService/getReport"
recordset = {}
global recordnum
def getReport(name , json):
	if (( json== 'json' ) or (json == True )): 
		json='.json'

	url="https://" + PRIMEBASEURL + PRIMEGETREPORTURLSTRING + json + '?reportTitle=' + name #+ ",async=true"
	print(url)
	r = requests.get(url, auth=(PRIMEUSER , PRIMEPWD))
	if r.status_code != 200:

		return "ERROR"

	if (json == '.json'):
	 	
		report = r.json()
		recordnum=0
		for line in report['mgmtResponse']['reportDataDTO'][0]['dataRows']['dataRow']:
			recordnum = recordnum +1
			recordset[ recordnum ] = {}
			for entry in line['entries']['entry']:
                		
				#print("Record" + str(recordnum) + entry['displayName'] + ": " + entry['dataValue'])
				key=entry['displayName']
				value=entry['dataValue']
				recordset[recordnum][key]=value


	else:

		report = r.text


	return recordset
