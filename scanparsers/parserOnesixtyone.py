#!/usr/bin/python3

import json, sys
from datetime import datetime

log_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def onesixtyone_parser(file, inputfilename):
	d = {}
	tempcom = ""
	d["log_time"] = log_time
	d["scanner"] = "onesixtyone"
	d["scanfile"] = inputfilename
	for line in file:
		if "Target ip read from command line" in line:
			ip = line.split()[6]
			d["ip"] = ip
		if "Trying community" in line:
			tempcom = line.split()[2].rstrip()
		if "[" in line and "]" in line:
			d["community_string"] = tempcom
			d["community_string_type"] = line.split()[1].replace("[","").replace("]","")
			d["message"] = line.rstrip()
#			print(json.dumps(d, indent=4))
#			print(json.dumps(d)+"\n")
#			yield(json.dumps(d, indent=4))
			yield(json.dumps(d)+"\n")
			# purge key/type for next passes
			try:
				del d["community_string"]
			except:
				pass
			try:
				del d["community_string_type"]
			except:
				pass
			try:
				del d["message"]
			except:
				pass

# TODO - write to output file
#with open(sys.argv[1], "r") as inputFile:
#	inputfilename = sys.argv[1]
#	onesixtyone_parser(inputFile, inputfilename)
#inputFile.close()
