#!/usr/bin/python3

import json, re, sys
from datetime import datetime

log_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def smbmap_share_parser(file, inputfilename):
	d = {}
	d["log_time"] = log_time
	d["scanner"] = "smbmap"
	d["scanfile"] = inputfilename
	for line in file:
		if "IP:" in line and "Name:" in line:
			ip = line.split()[2]
			try:
				ip = line.split()[2].split(":")[0]
				port = line.split()[2].split(":")[1]
				d["port"] = port
			except:
				pass
			d["ip"] = ip
		if re.match("^\t", line):
			if "Disk" not in line and "Permissions" not in line and "---" not in line:
				l = line.split("\t")
				share = l[1].rstrip()
				d["share"] = share
				share_permissions = l[2].rstrip()
				d["share_permissions"] = share_permissions
				# just print each share as it's own dict, makes parsing the next IP unneccessary
#				print(json.dumps(d, indent=4))
#				print(json.dumps(d)+"\n")
				yield(json.dumps(d)+"\n")


# TODO - write to output file
#with open(sys.argv[1], "r") as inputFile:
#	inputfilename = sys.argv[1]
#	smbmap_share_parser(inputFile, inputfilename)
#inputFile.close()
