#!/usr/bin/python3

import json, re, sys
from datetime import datetime

log_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# ipv4 support only
ip_check = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")

def snmpwalk_parser(file, inputfilename):
	d = {}
	d["log_time"] = log_time
	d["scanner"] = "snmpwalk"
	d["scanfile"] = inputfilename
	try:
		xx = inputfilename.split("/")
		for x in xx:
			if ip_check.match(x):
				ip = x
				d["ip"] = x
	except:
		pass
	for line in file:
		if " = " in line:
			l = line.replace("'","").replace('"','').split(" = ")
			try:
				if len(l[1]) > 2:
					mib = l[0]
					d["mib"] = mib
					mib_info = l[1].rstrip()
					d["mib_info"] = mib_info
					if "user" in inputfilename:
						try:
							username = line.split('"')[1]
							d["username"] = username
						except:
							pass
#					print(json.dumps(d, indent=4))
#					print(json.dumps(d)+"\n")
#					yield(json.dumps(d, indent=4))
					yield(json.dumps(d)+"\n")
			except:
				pass

# TODO - write to output file
#with open(sys.argv[1], "r") as inputFile:
#	inputfilename = sys.argv[1]
#	snmpwalk_parser(inputFile, inputfilename)
#inputFile.close()
