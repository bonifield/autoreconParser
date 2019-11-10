#!/usr/bin/python3

#===========================
#
# AutoRecon Parser
# v1.0 - 2019-11-10
# github.com/bonifield
# AutoRecon found at:  github.com/Tib3rius
#
# Parses "normal" logs found in the AutoRecon output hierarchy into JSON.
#
# This project is specifically intended to get logs into Splunk easier,
# though Elastic works great too if that's what you have.
#
#===========================


import glob, os, sys, timeit
from scanparsers.parserGobuster import gobuster_parser
from scanparsers.parserNbtscan import nbtscan_parser
from scanparsers.parserNiktoPlain import nikto_parser
from scanparsers.parserNmapSimple import nmap_simple_parser
from scanparsers.parserOnesixtyone import onesixtyone_parser
from scanparsers.parserOscanner import oscanner_parser
from scanparsers.parserPattern import pattern_parser
from scanparsers.parserSmbclient import smbclient_parser
from scanparsers.parserSmbmapList import smbmap_list_parser
from scanparsers.parserSmbmapShare import smbmap_share_parser
from scanparsers.parserSmtpuserenum import smtpuserenum_parser
from scanparsers.parserSnmpwalk import snmpwalk_parser
from scanparsers.parserWhatweb import whatweb_parser
from scanparsers.parserRobots import robots_parser


print()
print("USAGE:  autoreconParser.py [path-to-autorecon-output]")
print("\trun from the top-most folder above the individual IP output folders")
print()


files = glob.glob(sys.argv[1]+'/*/scans/*')


print("Starting to combine files.  This may take a minute...")
start = timeit.default_timer()
with open("master.json", "w") as masterFile:
	for i in files:

		if "gobuster" in i:
			with open(i, "r") as inputFile:
				for g in gobuster_parser(inputFile, i):
#					print(g)
					masterFile.write(g)
			inputFile.close()

		if "nbtscan" in i:
			with open(i, "r") as inputFile:
#				print(nbtscan_parser(inputFile, i))
				masterFile.write(nbtscan_parser(inputFile, i))
			inputFile.close()

		if "nikto" in i:
			with open(i, "r") as inputFile:
				for g in nikto_parser(inputFile, i):
#					print(g)
					masterFile.write(g)
			inputFile.close()

		if "nmap" in i:
			with open(i, "r") as inputFile:
				for g in nmap_simple_parser(inputFile, i):
#					print(g)
					masterFile.write(g)
			inputFile.close()

		if "onesixtyone" in i:
			with open(i, "r") as inputFile:
				for g in onesixtyone_parser(inputFile, i):
#					print(g)
					masterFile.write(g)
			inputFile.close()

		if "oracle_scanner" in i:
			with open(i, "r") as inputFile:
				for g in oscanner_parser(inputFile, i):
#					print(g)
					masterFile.write(g)
			inputFile.close()

		if "_pattern" in i:
			with open(i, "r") as inputFile:
#				print(pattern_parser(inputFile, i))
				masterFile.write(pattern_parser(inputFile, i))
			inputFile.close()

		if "robots" in i:
			with open(i, "r") as inputFile:
				for g in robots_parser(inputFile, i):
#					print(g)
					masterFile.write(g)
			inputFile.close()

		if "smbmap-list" in i:
			with open(i, "r") as inputFile:
				for g in smbmap_list_parser(inputFile, i):
#					print(g)
					masterFile.write(g)
			inputFile.close()

		if "smbclient" in i:
			with open(i, "r") as inputFile:
				for g in smbclient_parser(inputFile, i):
#					print(g)
					masterFile.write(g)
			inputFile.close()

		if "smbmap-share" in i:
			with open(i, "r") as inputFile:
				for g in smbmap_list_parser(inputFile, i):
#					print(g)
					masterFile.write(g)
			inputFile.close()

		if "smtp_user-enum" in i:
			with open(i, "r") as inputFile:
				for g in smtpuserenum_parser(inputFile, i):
#					print(g)
					masterFile.write(g)
			inputFile.close()

		if "snmpwalk" in i:
			with open(i, "r") as inputFile:
				for g in snmpwalk_parser(inputFile, i):
#					print(g)
					masterFile.write(g)
			inputFile.close()

		if "whatweb" in i:
			with open(i, "r") as inputFile:
#				print(whatweb_parser(inputFile, i))
				masterFile.write(whatweb_parser(inputFile, i))
			inputFile.close()

masterFile.close()
stop = timeit.default_timer()
print("Made master.json in {} seconds.".format(str(stop-start)))
print()
