#!/usr/bin/python3


import hashlib, json, re, sys
from datetime import datetime
from itertools import *


log_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# ipv4 support only
ip_check = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")


def whatweb_parser_worker(file, inputfilename):
	header_parse_mode = 0
	saved_position = 0
	d = {}
	for i, line in enumerate(file):
		#print(line)
		if line.strip():
			l = " ".join(line.split())
			#print(l)
			if "WhatWeb report for" in l:
				header_parse_mode = 0
				saved_position = i
				try:
					# this becomes the "current working object"
					url = l.split()[3]
					urlhash = hashlib.md5(url.encode('utf-8')).hexdigest()
					d[urlhash] = {}
					d[urlhash]["url"] = url
					d[urlhash]["log_time"] = log_time
					d[urlhash]["scanner"] = "whatweb"
					d[urlhash]["headers"] = ""
					d[urlhash]["scanfile"] = inputfilename
				except:
					pass
				try:
					http_host = url.split("/")[2].strip()
					d[urlhash]["http_host"] = http_host
				except:
					pass
				try:
					domain = http_host.split(":")[0].strip()
					d[urlhash]["domain"] = domain
					if ip_check.match(domain):
						d[urlhash]["url"]["ip"] = domain
				except:
					pass
				try:
					port = http_host.split(":")[1].strip()
					d[urlhash]["port"] = port
				except:
					pass
				try:
					uri = "/".join(url.split("/")[3:]).strip()
					if len(uri) > 0:
						d[urlhash]["uri"] = uri
				except:
					pass
				try:
					filename = url.split("/")[-1].strip()
					if filename != http_host:
						d[urlhash]["filename"] = filename
				except:
					pass
			if "Status : " in l:
				if i == saved_position + 1:
					try:
						http_status = " ".join(l.split()[2:]).strip()
						d[urlhash]["http_status"] = http_status
						http_status_code = http_status.split()[0].strip()
						d[urlhash]["http_status_code"] = http_status_code
						http_status_message = " ".join(http_status.split()[1:]).strip()
						d[urlhash]["http_status_message"] = http_status_message
					except:
						pass
			if "Title : " in l:
				if i == saved_position + 2:
					try:
						http_status_title = " ".join(l.split()[2:]).strip()
						d[urlhash]["http_status_title"] = http_status_title
					except:
						pass
			if "IP : " in l:
				if i == saved_position + 3:
					try:
						# TODO - IPv6 checks here
						ip = l.split(":")[1].strip()
						if not d[urlhash]["ip"] or "<Unknown>" not in ip:
							d[urlhash]["ip"] = ip
					except:
						pass
			if "Country : " in l:
				if i == saved_position + 4:
					try:
						country = " ".join(l.split()[2:]).strip()
						d[urlhash]["country"] = country
					except:
						pass
			if "Summary" in l and ":" in l:
				if i == saved_position + 6:
					try:
						summary = ":".join(l.split(":")[1:]).strip()
						d[urlhash]["summary"] = summary
					except:
						pass
			if "HTTP Headers:" in l:
				header_parse_mode = 1
			if header_parse_mode == 1:
				# lstrip to keep the trailing newline, but check if there's anything else there
				try:
					# this appends each line of the header to a single "headers" field value
					if len(line.lstrip()) > 1 and "HTTP Headers" not in l:
						d[urlhash]["headers"] += line.lstrip()
				except:
					pass
				if "HTTP/" in line:
					try:
						http_version = l.split("/")[1].split()[0]
						d[urlhash]["http_version"] = http_version
					except:
						pass
				if ":" in l and "HTTP Headers" not in l:
					try:
						h = l.split(":")
						hleft = str(h[0]).strip()
						if len(h) > 2:
							h[1] = ":".join(h[1:]).strip()
						hright = " ".join(h[1].split()).strip().replace("'","").replace('"','')
						d[urlhash]["http_"+hleft.lower()+"_key"] = hleft
						d[urlhash]["http_"+hleft.lower().strip()] = hright
					except:
						pass
	return(d)

def whatweb_parser(file, inputfilename):
	dd = whatweb_parser_worker(file, inputfilename) # dict "d" from whatweb_parser_worker()
	s = ""
	for k,v in dd.items():
		s += json.dumps(v)+"\n"
	return(s)
