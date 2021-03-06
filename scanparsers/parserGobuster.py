#!/usr/bin/python3

import json, re, sys
from datetime import datetime

log_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# ipv4 support only
ip_check = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")

def gobuster_parser(inputFile, inputfilename):
	for line in inputFile:
		d = {}
		d["log_time"] = log_time
		d["scanner"] = "gobuster"
		d["scanfile"] = inputfilename
		#l = line.split()
		try:
			url = line.split("(")[0].strip()
			d["url"] = url
		except:
			pass
		try:
			http_status = line.split("(")[1].split(")")[0].split()[-1].replace(")","").strip()
			d["http_status"] = http_status
		except:
			pass
		try:
			size = l[4].replace("]","").strip()
			d["size"] = size
		except:
			pass
		try:
			# ipv4 support only
			domain = url.split("/")[2].split(":")[0].strip()
			d["domain"] = domain
		except:
			pass
		try:
			# ipv4 support only
			if ip_check.match(domain):
				d["ip"] = domain.strip()
		except:
			pass
		try:
			# ipv4 support only
			http_host = url.split("/")[2].strip()
			d["http_host"] = http_host
		except:
			pass
		try:
			port = url.split("/")[2].split(":")[-1].strip()
			d["port"] = port
		except:
			pass
		try:
			uri = "/".join(url.split("/")[3:]).strip()
			d["uri"] = uri
		except:
			pass
		try:
			filename = url.split("/")[-1].strip()
			if len(filename) > 0:
				d["filename"] = filename
		except:
			pass
		try:
#			print(json.dumps(d, indent=4))
#			print(json.dumps(d))
#			return(json.dumps(d)+"\n")
#			yield(json.dumps(d, indent=4))
			yield(json.dumps(d)+"\n")
		except:
			pass


# TODO - write to output file
#with open(sys.argv[1], "r") as inputFile:
#	inputfilename = sys.argv[1]
##	for line in inputFile:
###	print(gobuster_parser(line, inputfilename))
#inputFile.close()
