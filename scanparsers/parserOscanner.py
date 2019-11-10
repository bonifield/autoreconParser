#!/usr/bin/python3

import json, sys
from datetime import datetime

log_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def oscanner_parser(file, inputfilename):
	d = {}
	ip = ""
	d["log_time"] = log_time
	d["scanner"] = "oscanner"
	d["scanfile"] = inputfilename
	d["service"] = "oracle"
	for line in file:
		l = line.split()
		if "Checking host" in line:
			ip = l[3].rstrip()
			d["ip"] = ip
		if "is locked" in line:
			l = line.split()
			d["ip"] = ip
			d["username"] = l[2].split("/")[0]
			d["password"] = l[2].split("/")[1]
			d["exists"] = "yes"
			d["locked"] = "yes"
#			print(json.dumps(d, indent=4))
#			print(json.dumps(d)+"\n")
#			yield(json.dumps(d, indent=4))
			yield(json.dumps(d)+"\n")
			# purge creds for next lines
			try:
				del d["username"]
				del d["password"]
				del d["exists"]
				del d["locked"]
			except:
				pass
		if "Account" in line and "found" in line:
			l = line.split()
			d["ip"] = ip
			d["username"] = l[2].split("/")[0]
			d["password"] = l[2].split("/")[1]
			d["exists"] = "yes"
#			print(json.dumps(d, indent=4))
#			print(json.dumps(d)+"\n")
#			yield(json.dumps(d, indent=4))
			yield(json.dumps(d)+"\n")
			# purge creds for next lines
			try:
				del d["username"]
				del d["password"]
				del d["exists"]
			except:
				pass


# TODO - write to output file
#with open(sys.argv[1], "r") as inputFile:
#	inputfilename = sys.argv[1]
#	oscanner_parser(inputFile, inputfilename)
#inputFile.close()
