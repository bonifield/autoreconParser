## New Splunk configs, dashboards, saved searches, queries, etc will be placed here as they are created
- savedsearches.conf
  - an export of some basic queries to help load results; see below for usage, where to place the conf, etc
- splunk-recon-lookup-notes.txt
  - notes file with the saved searches that can be run manually, with some other bits of userful information
  - please note that you should omit the outputlookup statements unless you absolutely want to change the table; alternatively, use append=true if you wish to new unique data (ensure any scheduled searches won't overwrite it though)

### To Do
- add dashboards, more queries, methods to tie the fields together, streamline names in Splunk lookups

# Instructions
## It looks like a lot, but it's a 5-minute process (or less if you're already familiar with Splunk)
### Install Splunk
- I've previously gone over those instructions **[here](https://github.com/bonifield/splunk_on_security_onion/blob/master/README.md)**
- tl;dr
```
sudo dpkg -i [yoursplunkfile].deb
sudo /opt/splunk/bin/splunk start
- Log into the Splunk GUI, and configure the server to use HTTPS
Settings --> Server Settings --> General Settings --> Enable SSL (HTTPS) in Splunk Web? --> YES
- Make the new indexes viewable on the homepage Data Summary and for any user account deemed necessary
Settings --> Access Controls --> Roles --> [role] --> Indexes tab --> select the checkboxes in both Included and Default for desired index
```

### After install, place savedsearches.conf where Splunk can find it, then restart Splunk
_ALTERNATIVELY, you can manually add the saved searches which are saved in [splunk-recon-lookup-notes.txt](https://github.com/bonifield/autoreconParser/blob/master/splunkconfigs/splunk-recon-lookup-notes.txt) by going to Settings --> "Searches, reports, and alerts" --> New Report (top-right corner)_
```
sudo cp savedsearches.conf /opt/splunk/etc/apps/search/local/savedsearches.conf
sudo /opt/splunk/bin/splunk restart
```

### Create an index named "recon":
- use all defaults unless you really know what you're doing
```
Settings --> Indexes --> New Index (top-right corner)
Index Name:  recon
Save
```

### Start Splunk and add data, while also making a custom sourcetype "recon_json" (or choose your own name):
- if you data does not immediately preview for you, you may not have enough disk space in your VM
- don't forget to select the right index!
```
Settings --> Add Data --> Upload
Select File, "master.json"
> Next
Source type should auto-populate to _json, just "Save As" and make it "recon_json".  The data should preview on the right.
> Next
Host field value:  autoreconParser
Index:  recon
> Review
Submit
(then Start Searching to verify it appeared how you want, or else continue to the next step)
```

### Run the saved searches to make easier tables to look at and load for dashboard panels, etc
- if you plan on ingesting data regularly with autoreconParser, schedule the jobs under Edit --> Schedule (paid Splunk)
```
Settings --> Searches, reports, and alerts --> Filter by Owner "recon_"
> Run
(yes, run all of them at least once, and again after adding new data if unscheduled)
```

### Add the Recon Overview dashboard
- you MUST run the saved searches because they fuel the dashboard panels
- if using the paid version of Splunk, feel free to convert the code to the saved search results directly (because scheduling them will automate that much more of your life)
```
Top Ribbon --> Dashboards --> Create New Dashboard
Title:  Recon Overview
Permissions:  Shared in App
> Create Dashboard
Edit Dashboard --> Source (top-left corner)
Paste the dashboard XML
> Save (top-right corner)
```

## Randoms
### Use the lookup tables (or definitions if desired) to fuel dashboard panels for near-instant results
- pairs well with scheduled jobs to update the tables
- creating a lookup definition, based on the associated lookup table, is necessary for automatic lookups (tl;dr enrichment)
- yes, there is a leading pipe
#### load the table on the search command line or in a dashboard query tag
```
| inputlookup recon_GobusterWebPaths.csv
| inputlookup recon_NbtscanMacHostnamesDomainInfo.csv
| inputlookup recon_NiktoVulnInfo.csv
| inputlookup recon_NmapSimpleInfo.csv
| inputlookup recon_OnesixtyoneCommunityStrings.csv
| inputlookup recon_OscannerUsersPasswords.csv
| inputlookup recon_PatternsVulns.csv
| inputlookup recon_RobotsDisallowed.csv
| inputlookup recon_SmbclientShareWorkgroupInfo.csv
| inputlookup recon_SmbmapIpPortSharePermissions.csv
| inputlookup recon_SmbmapShareFilesInfo.csv
| inputlookup recon_SnmpwalkUsersInfo.csv
| inputlookup recon_WhatwebHttpHeaders.csv
```
#### if using a scheduled Saved Search, load the results directly
```
| loadjob savedsearch="YOUR-USERNAME:APPLICATION-NAME:REPORT-NAME"

ex. load a job in the Search app context, which is owned by "nobody"
| loadjob savedsearch="nobody:search:recon_NmapSimpleInfo"
```

### Troubleshooting
- data not previewing when uploading new files: your VM is likely running low on disk space, make sure there is 5GB+
