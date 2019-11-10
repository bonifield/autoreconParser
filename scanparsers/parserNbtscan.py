#!/usr/bin/python3

import json, re, sys
from datetime import datetime

log_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def nbtscan_parser(file, inputfilename):
	d = {}
	d["log_time"] = log_time
	d["scanner"] = "snmpwalk"
	d["scanfile"] = inputfilename
#	d["ip"] = inputfilename.split("/")[0]
	for line in file:
		if "NetBIOS Name Table for" in line:
			try:
				ip = line.split()[5].split(":")[0]
				d["ip"] = ip
			except:
				pass
		if "Adapter address" in line:
			try:
				mac = line.split("address: ")[1].rstrip()
				d["mac"] = mac
			except:
				pass
		if "Workstation Service" in line:
			try:
				hostname = line.split()[0]
				d["hostname"] = hostname
			except:
				pass
		if "Domain Name" in line:
			try:
				domain = line.split()[0]
				d["domain"] = domain
			except:
				pass
		if "Domain Controllers" in line:
			try:
				domain_controller_name = line.split()[0]
				d["domain_controller_name"] = domain_controller_name
			except:
				pass
		if "File Server Service" in line:
			try:
				file_server_service = line.split()[0]
				d["file_server_service"] = file_server_service
			except:
				pass
#		if line.rstrip():
#			if "Name" not in line and "Service" not in line and "Type" not in line and "-----" not in line and "Doing NBT name scan" not in line:
#				print(line)

#	print(json.dumps(d, indent=4))
#	print(json.dumps(d)+"\n")
#	return(json.dumps(d, indent=4))
	return(json.dumps(d)+"\n")


# TODO - write to output file
#with open(sys.argv[1], "r") as inputFile:
#	inputfilename = sys.argv[1]
#	nbtscan_parser(inputFile, inputfilename)
#inputFile.close()
