#!/usr/bin/python3

import json, re, sys
from datetime import datetime

log_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# ipv4 support only
ip_check = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")

def robots_parser(inputFile, inputfilename):
	ip = ""
	try:
		xx = inputfilename.split("/")
		for x in xx:
			if ip_check.match(x):
				ip = x
	except:
		pass
	d = {}
	d["log_time"] = log_time
	d["scanner"] = "robots"
	d["scanfile"] = inputfilename
	if len(ip) > 2:
		d["ip"] = ip
	for line in inputFile:
		if "Disallow: " in line:
			l = line.split("Disallow: ")[1].rstrip()
			d["disallowed"] = l
			# add uri as duplicate value, matches other naming conventions
			d["uri"] = l
			d["is_disallowed"] = "yes"
#			yield(json.dumps(d, indent=4))
			yield(json.dumps(d)+"\n")
#			return(json.dumps(d, indent=4))
#			return(json.dumps(d)+"\n")

# TODO - write to output file
#with open(sys.argv[1], "r") as inputFile:
#	inputfilename = sys.argv[1]
#	print(robots_parser(line, inputfilename))
#inputFile.close()

