#!/usr/bin/python3

import json, sys
from datetime import datetime

log_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def smtpuserenum_parser(file, inputfilename):
	d = {}
	tempcom = ""
	d["log_time"] = log_time
	d["scanner"] = "smtp-user-enum"
	d["scanfile"] = inputfilename
	d["port"] = 25
	d["service"] = "smtp"
	for line in file:
		if "Scan started at" in line:
			line = " ".join(line.split())
			l = line.split()
			d["start_time"] = " ".join(l[4:9])
		if "exists" in line:
			l = line.split()
			d["ip"] = l[0].split(":")[0]
			d["username"] = l[1]
			d["exists"] = "yes"
#			print(json.dumps(d, indent=4))
#			print(json.dumps(d)+"\n")
#			yield(json.dumps(d, indent=4))
			yield(json.dumps(d)+"\n")
			# purge ip and username for next lines
			try:
				del d["ip"]
			except:
				pass
			try:
				del d["username"]
			except:
				pass
			try:
				del d["exists"]
			except:
				pass

# TODO - write to output file
#with open(sys.argv[1], "r") as inputFile:
#	inputfilename = sys.argv[1]
#	for g in smtpuserenum_parser(inputFile, inputfilename):
#		print(g)
#inputFile.close()
