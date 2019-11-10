#!/usr/bin/python3

import json, re, sys
from datetime import datetime

log_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# ipv4 support only
ip_check = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
#pipe_check = re.compile("^\|")


def nmap_simple_parser(file, inputfilename):
#	port_parse_mode = 0
#	service_info = ""
#	pipelist = []
	d = {}
	d["log_time"] = log_time
	d["scanner"] = "nmap"
	d["scanfile"] = inputfilename
	for line in file:
		l = " ".join(line.split())
		# basic line descriptions
		if "Nmap scan report for" in l:
			try:
				ip = l.split()[4]
				d["ip"] = ip
			except:
				pass
		if "Scanned at" in l:
			try:
				start_time = str(l.split()[2]+" "+l.split()[3])
				d["start_time"] = start_time
				timezone = l.split()[4]
				d["timezone"] = timezone
				duration = l.split()[6]
				d["duration"] = duration
			except:
				pass
		if "open" in l and "/" in l:
			try:
				port = l.split()[0].split("/")[0]
				d["port"] = int(port)
			except:
				pass
			try:
				protocol = l.split()[0].split("/")[1]
				d["protocol"] = protocol
			except:
				pass
			try:
				state = l.split()[1]
				d["state"] = state
			except:
				pass
			try:
				service = l.split()[2]
				d["service"] = service
#				service_info = service # save the service before continuing downward
#				port_parse_mode = 1 # flip on the pipe parser which should hit on the next line if present
			except:
				pass
			if "no-response" in line:
				d["reason"] = "no-response"
			if "ttl" in line:
				try:
					reason = " ".join(l.split()[3:6])
					d["reason"] = reason
				except:
					pass
				try:
					version = " ".join(l.split()[6:])
					d["version"] = version
				except:
					pass

			if d["port"]:
				if type(d["port"]).__name__ == "int":
#					print(json.dumps(d, indent=4))
#					print(json.dumps(d)+"\n")
#					yield(json.dumps(d, indent=4))
					yield(json.dumps(d)+"\n")



# TODO - write to output file
#with open(sys.argv[1], "r") as inputFile:
#	inputfilename = sys.argv[1]
#	g = nmap_simple_parser(inputFile, inputfilename)
#	for x in g:
#		print(x)
###	print(nmap_simple_parser(inputFile, inputfilename))
#inputFile.close()
