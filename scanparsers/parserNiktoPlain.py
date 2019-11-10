#!/usr/bin/python3

import json, sys
from datetime import datetime
from itertools import *

log_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def nikto_parser(file, inputfilename):
	d = {}
	d["log_time"] = log_time
	d["scanner"] = "nikto"
	d["scanfile"] = inputfilename
	for i, line in enumerate(file):
		if "-------" not in line:
			if "Target IP:" in line:
				try:
					ip = line.split()[3]
					d["ip"] = ip
				except:
					pass
			if "Target Hostname:" in line:
				try:
					hostname = line.split()[3]
					d["hostname"] = hostname
				except:
					pass
			if "Target Port:" in line:
				try:
					port = line.split()[3]
					d["port"] = port
				except:
					pass
			if "Start Time:" in line:
				try:
					start_time = str(line.split()[3]+" "+line.split()[4])
					d["start_time"] = start_time
					timezone = line.split()[5].replace("(","").replace(")","")
				except:
					pass
#			if "End Time:" in line:
#				try:
#					end_time = " ".join([line.split()[3], line.split()[4]])
#					d["end_time"] = end_time
#					duration = line.split()[6].replace("(","").replace(")","")
#					d["duration"] = duration
#					maxmarker = i
#				except:
#					pass
			if i > 6:
				try:
					message = " ".join(line.lstrip().replace("+ ","").replace("'","").replace('"','').rstrip().split())
					d["message"] = 	message
					if "OSVDB" in message:
						try:
							vuln_id = message.split(":")[0]
							d["vuln_id"] = vuln_id
						except:
							pass
					else:
						try:
							del d["vuln_id"]
						except:
							pass
				except:
					pass
#				yield(json.dumps(d, indent=4))
				yield(json.dumps(d)+"\n")

# TODO - write to output file
#with open(sys.argv[1], "r") as inputFile:
#	inputfilename = sys.argv[1]
#	g = nikto_parser(inputFile, inputfilename)
#	for x in g:
#		print(x)
#inputFile.close()
