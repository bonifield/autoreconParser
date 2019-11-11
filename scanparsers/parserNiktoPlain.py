#!/usr/bin/python3

#
# TODO - reset dictionary on each pass after line 6 (preserve IP, port, etc but dump everything else)
#

import json, sys
from datetime import datetime
from itertools import *

log_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def nikto_parser(file, inputfilename):
	d = {}
	d["log_time"] = log_time
	d["scanner"] = "nikto"
	d["scanfile"] = inputfilename
	for i, line in enumerate(file):
		if "-------" not in line:
			if "Target IP:" in line:
				try:
					ip = line.split()[3]
					d["ip"] = ip
				except:
					pass
			if "Target Hostname:" in line:
				try:
					hostname = line.split()[3]
					d["hostname"] = hostname
				except:
					pass
			if "Target Port:" in line:
				try:
					port = line.split()[3]
					d["port"] = port
				except:
					pass
			if "Start Time:" in line:
				try:
					start_time = str(line.split()[3]+" "+line.split()[4])
					d["start_time"] = start_time
					timezone = line.split()[5].replace("(","").replace(")","")
				except:
					pass
#			if "End Time:" in line:
#				try:
#					end_time = " ".join([line.split()[3], line.split()[4]])
#					d["end_time"] = end_time
#					duration = line.split()[6].replace("(","").replace(")","")
#					d["duration"] = duration
#					maxmarker = i
#				except:
#					pass
			if i > 6:
				# BETTER RESET GOES HERE
				try:
					message = " ".join(line.strip().replace("+ ","").replace("'","").replace('"','').strip().split())
					d["message"] = 	message
					if "OSVDB" in message:
						try:
							m = message.strip().split(": ")
							vuln_id = m[0].strip()
							if "OSVDB" in vuln_id:
								d["vuln_id"] = vuln_id
							if len(m) == 2:
								reason = m[1].strip()
								d["reason"] = reason
							elif len(m) > 2:
								if len(m[0].split()) == 1:
									if len(m[1].split()) == 1:
										if "/" in m[1]:
											uri = m[1].strip()
											d["uri"] = uri
											reason = m[2].strip()
											d["reason"] = reason
						except:
							pass
					else:
						try:
							del d["vuln_id"]
						except:
							pass
######################################################
					if "/" in message and ":" in message and "ERROR" not in message and "OSVDB" not in message and "does not match" not in message and "appears to be outdated" not in message and "Multiple index files found" not in message and "Issuer" not in message and "leaks inodes" not in message and "Retrieved " not in message:
						try:
							m = message.strip().split(": ")
							if len(m) == 2:
								if len(m[0].split()) == 1:
									uri = m[0].strip()
									if uri != "Server":
										d["uri"] = uri
										reason = m[1].strip()
										d["reason"] = reason
						except:
							pass
					if "/" in message and "Entry" in message and "returned a non-forbidden or redirect" in message and "robots.txt" in message and "Illegal" not in message and "appears to be outdated" not in message and "Multiple index files found" not in message and "OSVDB" not in message and "leaks inodes" not in message and "Retrieved " not in message:
						try:
							uri = message.split()[1].strip()
							d["uri"] = uri
							reason = str("Entry in robots.txt returned " + message.split("returned ")[1]).strip()
							d["reason"] = reason
						except:
							pass
					if "/" in message and "Multiple index files found" in message:
						try:
							reason = message.split(":")[0].strip()
							d["reason"] = reason
							try:
								del d["uri"]
							except:
								pass
						except:
							pass
					if "Issuer:" in message and "=" in message and "appears to be outdated" not in message and "OSVDB" not in message:
						try:
							certificate_issuer = message.strip().split(": ")[1].strip()
							d["certificate_issuer"] = certificate_issuer
							try:
								cert_cn = certificate_issuer.split("/CN=")[1].split("/")[0].strip()
								d["cert_cn"] = cert_cn
							except:
								pass
							try:
								cert_st = certificate_issuer.split("/ST=")[1].split("/")[0].strip()
								d["cert_st"] = cert_st
							except:
								pass
							try:
								cert_l = certificate_issuer.split("/L=")[1].split("/")[0].strip()
								d["cert_l"] = cert_l
							except:
								pass
							try:
								cert_o = certificate_issuer.split("/O=")[1].split("/")[0].strip()
								d["cert_o"] = cert_o
							except:
								pass
							try:
								cert_ou = certificate_issuer.split("/OU=")[1].split("/")[0].strip()
								d["cert_ou"] = cert_ou
							except:
								pass
							try:
								cert_email = certificate_issuer.split("/emailAddress=")[1].strip()
								d["cert_email"] = cert_email
								d["email"] = cert_email
								try:
									cert_email = cert_email.split("/")[0].strip()
									d["cert_email"] = cert_email
									d["email"] = cert_email
								except:
									pass
							except:
								pass
							try:
								del d["uri"]
							except:
								pass
							try:
								del d["reason"]
							except:
								pass
						except:
							pass
					else:
						try:
							del d["certificate_issuer"]
						except:
							pass
						try:
							del d["cert_cn"]
						except:
							pass
						try:
							del d["cert_st"]
						except:
							pass
						try:
							del d["cert_l"]
						except:
							pass
						try:
							del d["cert_o"]
						except:
							pass
						try:
							del d["cert_ou"]
						except:
							pass
						try:
							del d["cert_email"]
						except:
							pass
						try:
							del d["email"]
						except:
							pass
					if "appears to be outdated" in message and "OSVDB" not in message:
						try:
							d["outdated"] = "yes"
							try:
								del d["uri"]
							except:
								pass
							try:
								del d["reason"]
							except:
								pass
						except:
							pass
					else:
						try:
							del d["outdated"]
						except:
							pass
######################################################
				except:
					pass
#				yield(json.dumps(d, indent=4))
				yield(json.dumps(d)+"\n")

# TODO - write to output file
#with open(sys.argv[1], "r") as inputFile:
#	inputfilename = sys.argv[1]
#	g = nikto_parser(inputFile, inputfilename)
#	for x in g:
#		print(x)
#inputFile.close()
