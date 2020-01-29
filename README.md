# autoreconParser
Parses various scan outputs into JSON, meant to be used with the awesome [AutoRecon](https://github.com/Tib3rius/AutoRecon) or artifacts in a matching directory structure.  Optional Splunk content to help with the artifact analysis is included in the [splunkconfigs folder](https://github.com/bonifield/autoreconParser/tree/master/splunkconfigs).

## Fixes
```
v1.0.2 - 2020-01-28
- updated WhatWeb parser and main script, fixed multiple issues with GoBuster parser
- Splunk dashboard updates

v1.0.1 - 2020-01-24
- added epoch timestamps to the output filename

v1.0 - 2019-11-10
- initial release
```

## Usage
```
autoreconParser.py [path-to-autorecon-output]
- run from the top-most directory above the individual IP output folders, ex. autoreconParser.py /path/to/autoreconoutputs/
```

### note *most* of the outputs are supported, there are still a few in progress (see below)
## Supported Scanner Outputs (plaintext and named as generated by AutoRecon)
- gobuster
- nbtscan
- nikto
- nmap (simple port/protocol/service/state/reason output, no pipe-leading service scanners)
- onesixtyone
- oscanner (Oracle Scanner)
- _patterns.txt (generated by AutoRecon, hits some highlights in the scans)
- robots.txt (as collected from a webserver)
- smbclient
- smbmap (list and share output)
- smtp-user-enum
- snmpwalk
- whatweb

## Not Yet Supported (but coming soon)
- enum4linux
- nmap script outputs
- showmount
- sslscan
- svwar
- wpscan

## Known Issues
- let me know

### Requirements
- [AutoRecon](https://github.com/Tib3rius/AutoRecon) by [Tib3rius](https://github.com/Tib3rius/)
  - The version tested with this project is backed up as AutoRecon-master-20191110.zip in this repo, nothing in that project was altered for this one.
- OR
- Plaintext output from your preferred scanner, following the folder hierarchy IPADDRESS/scans/YOURSCAN.txt
	- this was built with AutoRecon in mind, so you may have to make your own alterations

### Fields Generated
```
anonymous_ftp_login
certificate_issuer
cert_* (attempts to parse fields from a certificate, ex. cert_cn, cert_ou etc)
community_string
community_string_type
country
disallowed
domain
domain_controller_name
duration
email (still in progress, Nikto certs only)
exists
file_date
filename
file_permissions
file_server_service
headers
hostname
http_* (header fields values, ex. http_content-type = text/html)
http_host
http_*_key (preserved header field keys, ex. http_content-type_key = Content-Type)
http_status
http_status_title
ip
is_disallowed
locked
log_time
mac
message
mib
mib_info
pattern
outdated
port
potentially_vulnerable
protocol
reason
scanfile (the log file and path)
scanner
service
share
share_permissions
share_type
size
start_time
state
subfolder
summary
timezone
uri
url
username
version
vuln_id
workgroup
workgroup_master
*_info (services, ex. ftp_info)
```

### To Do
- add switch for individual file parsing or whole directory
- the Nmap basic parser doesn't purge the version from the previous line that had one if the current one does not (must fix!)
- add _commands.log output and timestamps wherever possible
- fix Nikto dictionary parsing after line 6 before each yield (better soft reset vs try/except del statements)
- add Nmap script parsing
- finish up the rest of the parsers
- get MAC addresses from Nmap scans (oops!)
- parse out emails from fields already collected (oops!)
- clean up the excessive try/except statements
	- grab errors and write them somewhere for additional processing
- make alternate version for reading all logs in a directory, NOT locked into the ip/scans/* format
- add Splunk content
	- dashboards, saved searches, macros, queries, reports, etc
	- setup instructions for Splunk content
- better "message" field parsing for additional details when available
- better field synchronization when possible
