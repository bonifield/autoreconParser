#!/usr/bin/python3

import json, re, sys
from datetime import datetime
from itertools import *

log_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# ipv4 support only
ip_check = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")


def whatweb_parser(file, inputfilename):
	header_parse_mode = 0
	d = {}
	d["log_time"] = log_time
	d["scanner"] = "whatweb"
	d["headers"] = ""
	d["scanfile"] = inputfilename
	for i, line in enumerate(file):
		if line.strip():
			l = " ".join(line.split())
			if "WhatWeb report for" in l:
				try:
					url = l.split()[3]
					d["url"] = url
				except:
					pass
				try:
					http_host = url.split("/")[2]
					d["http_host"] = http_host
				except:
					pass
				try:
					domain = http_host.split(":")[0]
					d["domain"] = domain
					if ip_check.match(domain):
						d["ip"] = domain
				except:
					pass
				try:
					port = http_host.split(":")[1]
					d["port"] = port
				except:
					pass
				try:
					uri = "/".join(url.split("/")[3:]).strip()
					if len(uri) > 0:
						d["uri"] = uri
				except:
					pass
				try:
					filename = url.split("/")[-1].strip()
					if filename != http_host:
						d["filename"] = filename
				except:
					pass
			if "Status : " in l:
				try:
					http_status = " ".join(l.split()[2:]).strip()
					d["http_status"] = http_status
				except:
					pass
			if "Title : " in l:
				try:
					http_status_title = " ".join(l.split()[2:]).strip()
					d["http_status_title"] = http_status_title
				except:
					pass
			if "Country : " in l:
				try:
					country = " ".join(l.split()[2:])
					d["country"] = country
				except:
					pass
			if "Summary : " in l:
				try:
					summary = " ".join(l.split()[2:])
					d["summary"] = summary
				except:
					pass
			if header_parse_mode == 1:
				# lstrip to keep the trailing newline, but check if there's anything else there
				try:
					if len(line.lstrip()) > 1
						d["headers"] += line.lstrip()
				except:
					pass
				if "HTTP/" in line:
					try:
						http_version = l.split("/")[1].split()[0]
					except:
						pass
				if ":" in line:
					try:
						x = l.split(":")
						d["http_"+x[0].lower().strip()+"_key"] = x[0].strip()
						d["http_"+x[0].lower().strip()] = " ".join(x[1].split()).strip().replace("'","").replace('"','')
					except:
						pass
			if "HTTP Headers:" in l:
				header_parse_mode = 1
#	return(json.dumps(d, indent=4))
	return(json.dumps(d)+"\n")


# TODO - write to output file
#with open(sys.argv[1], "r") as inputFile:
#	inputfilename = sys.argv[1]
#	print(whatweb_parser(inputFile, inputfilename))
##	for line in inputFile:
##		x = whatweb_parser(line)
##		if x:
##			print(x)
#inputFile.close()
