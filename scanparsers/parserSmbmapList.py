#!/usr/bin/python3

import json, re, sys
from datetime import datetime

log_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def smbmap_list_parser(file, inputfilename):
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
				l = line.lstrip().split("\t")
				x = line.split() # for counting fields, cheap way to find if file or folder
				if len(l) == 2 and len(x) < 8:
					share = l[0].rstrip()
					d["share"] = share
					share_permissions = l[1].rstrip()
					d["share_permissions"] = share_permissions
					# attempt to clean up any filename keys when hitting a new share
					try:
						del d["filename"]
					except:
						pass
					try:
						del d["file_permissions"]
					except:
						pass
					try:
						del d["subfolder"]
					except:
						pass
					# just print each share as it's own dict, makes parsing the next IP unneccessary
#					print(json.dumps(d, indent=4))
#					print(json.dumps(d)+"\n")
					yield(json.dumps(d)+"\n")
				elif len(x) >= 8:
					try:
						filename = " ".join(x[7:]).rstrip()
						if filename != "." and filename != "..":
							d["filename"] = filename
							file_permissions = x[0]
							d["file_permissions"] = file_permissions
#							print(json.dumps(d, indent=4))
#							print(json.dumps(d)+"\n")
							yield(json.dumps(d)+"\n")
					except:
						pass
				elif len(x) == 1:
					try:
						subfolder = x[0]
						d["subfolder"] = subfolder
						# skip printing here because the subfolder will get picked up before the filenames and stored in the dictionary
#						print(json.dumps(d, indent=4))
#						print(json.dumps(d)
					except:
						pass


# TODO - write to output file
#with open(sys.argv[1], "r") as inputFile:
#	inputfilename = sys.argv[1]
#	smbmap_list_parser(inputFile, inputfilename)
#inputFile.close()
