#!/usr/bin/python3

import json, re, sys
from datetime import datetime

log_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# ipv4 support only
ip_check = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")

def pattern_parser(file, inputfilename):
	d = {}
	# ip depends on the file path!!!
	try:
		xx = inputfilename.split("/")
		for x in xx:
			if ip_check.match(x):
				ip = x
				d["ip"] = ip
	except:
		pass
	d["log_time"] = log_time
	d["scanner"] = "autorecon-patterns"
	d["scanfile"] = inputfilename
	d["service"] = "oracle"
	listy = []
	for line in file:
		if line.rstrip():
			line = line.replace("'","SINGLEQUOTE").replace('"','DOUBLEQUOTE').rstrip()
			listy.append(line)
			if "VULNERABLE" in line:
				d["potentially_vulnerable"] = "yes"
			if "Anonymous FTP Enabled" in line:
				d["anonymous_login"] = "yes"
				d["potentially_vulnerable"] = "yes"
			if "WebDAV is enabled" in line:
				d["potentially_vulnerable"] = "yes"
			if "Tomcat" in line:
				d["potentially_vulnerable"] = "yes"
			if "CS-Cart" in line:
				d["potentially_vulnerable"] = "yes"
			if "Identified HTTP Server" in line:
				d["http_server"] = line.split("HTTP Server: ")[1].rstrip()
	d["pattern"] = "\n".join(listy)
#	print(json.dumps(d, indent=4))
#	print(json.dumps(d)+"\n")
#	return(json.dumps(d, indent=4))
	return(json.dumps(d)+"\n")


# TODO - write to output file
#with open(sys.argv[1], "r") as inputFile:
#	inputfilename = sys.argv[1]
#	pattern_parser(inputFile, inputfilename)
#inputFile.close()
