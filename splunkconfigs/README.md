### Install Splunk
- I've previously gone over those instructions **[here](https://github.com/bonifield/splunk_on_security_onion/blob/master/README.md)**

### After install, but before running Splunk, place savedsearches.conf here (substitute /opt/splunk for whatever $SPLUNK_HOME you set if doing something custom:
```
/opt/splunk/etc/apps/search/local/savedsearches.conf
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
```

### Use the lookup tables (or definitions if desired) to fuel dashboard panels for near-instant results
- pairs well with scheduled jobs to update the tables
- creating a lookup definition, based on the associated lookup table, is necessary for automatic lookups (tl;dr enrichment)
- yes, there is a leading pipe
#### on the search command line
```
a
```
