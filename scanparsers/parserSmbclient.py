#!/usr/bin/python3

import json, re, sys
from datetime import datetime

log_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# ipv4 support only
ip_check = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")

def smbclient_parser(file, inputfilename):
	d = {}
	d["log_time"] = log_time
	d["scanner"] = "smbclient"
	d["scanfile"] = inputfilename
	try:
		xx = inputfilename.split("/")
		for x in xx:
			if ip_check.match(x):
				ip = x
				d["ip"] = ip
	except:
		pass
	# three modes
	sharename_mode = 0
	server_mode = 0
	workgroup_mode = 0
	for line in file:
		# purge keys from the dict on each line to clean it up
#		try:
#			del d[""]
#		except:
#			pass
		if "Sharename" in line and "Type" in line and "Comment" in line:
#			print("SHARENAME MODE ACTIVATED")
			sharename_mode = 1
			server_mode = 0
			workgroup_mode = 0
		if "Server" in line and "Comment" in line:
#			print("SERVER MODE ACTIVATED")
			sharename_mode = 0
			server_mode = 1
			workgroup_mode = 0
		if "Workgroup" in line and "Master" in line:
#			print("WORKGROUP MODE ACTIVATED")
			sharename_mode = 0
			server_mode = 0
			workgroup_mode = 1
		if sharename_mode == 1:
			if "---" not in line and "Sharename" not in line and "Type" not in line and "Comment" not in line:
				if line.strip():
					l = line.split("\t")
					if len(l) >= 2:
#						print(l)
						tablist = l[1].rstrip().replace("  ","\t").split("\t")
						xlist = [i for i in tablist if len(i)>0]
#						print(xlist)
##						x = l[1].split()
						share = xlist[0]
						d["share"] = share
						share_type = xlist[1]
						d["share_type"] = share_type
						try:
							message = xlist[2]
							d["message"] = message
						except:
							pass
#						print(json.dumps(d, indent=4))
#						print(json.dumps(d)+"\n")
						yield(json.dumps(d)+"\n")
		if server_mode == 1:
			if "---" not in line and "Server" not in line and "Comment" not in line:
				if line.strip():
					l = line.split("\t")
					if len(l) >= 2:
#						print(l)
						x = l[1].split()
						hostname = x[0]
						d["hostname"] = hostname
						message = " ".join(x[1:])
						d["message"] = message
#						print(json.dumps(d, indent=4))
#						print(json.dumps(d)+"\n")
						yield(json.dumps(d)+"\n")
		if workgroup_mode == 1:
			if "---" not in line and "Workgroup" not in line and "Master" not in line:
				if line.strip():
					l = line.split("\t")
					if len(l) >= 2:
#						print(l)
						x = l[1].split()
						workgroup = x[0]
						d["workgroup"] = workgroup
						workgroup_master = " ".join(x[1:])
						d["workgroup_master"] = workgroup_master
#						print(json.dumps(d, indent=4))
#						print(json.dumps(d)+"\n")
						yield(json.dumps(d)+"\n")

#					print(json.dumps(d, indent=4))
#					print(json.dumps(d)+"\n")


# TODO - write to output file
#with open(sys.argv[1], "r") as inputFile:
#	inputfilename = sys.argv[1]
#	smbclient_parser(inputFile, inputfilename)
#inputFile.close()
