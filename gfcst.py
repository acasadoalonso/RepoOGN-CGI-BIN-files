#!/usr/bin/python
import cgi
import os
import cgitb
import urllib2

from xml.etree.ElementTree import parse, fromstring
import sys
import datetime

form=cgi.FieldStorage()
print("Content-type: text/html\n")

#html1="""<HTML><TITLE>Get the meteo information</TITLE> <IMG src="gif/ogn-logo-150x150.png" border=1 alt=[image]><H1>The meteo observations for the selected ICAO station are: </H1> <HR> <P> %s </P> </HR> """
html1="""<HTML><TITLE>Get the meteo information</TITLE> <IMG src="../gif/ogn-logo-150x150.png" border=1 alt=[image]><H1>The meteo observations for the selected ICAO station (%s) are: </H1> """
html2="""<center><table><tr><td><pre>"""
html3="""</pre></td></tr></table></center></html>"""

www=True
sta="LEMD"
if not 'station' in form:                             # check if registrtion is provided
        print "Maddrid (LEMD) by default"
else:
	sta=form['station'].value                      # get the ICAO ID

if www: print (html1 % sta)
if www: print html2
################

print "<a> TAFOR </a>"
url =('https://aviationweather.gov/adds/dataserver_current/httpparam?dataSource=tafs&requestType=retrieve&format=xml&stationString=%s&hoursBeforeNow=25' % sta)
f = urllib2.urlopen(url)
root = parse(f)

fc = list(root.iterfind('data/TAF'))
print "<a> ", fc," </a>"
for taf in fc:
    rawtext=taf.findtext('raw_text')
    print '<a>', rawtext, '</a>' 
f.close()
if www: print html3
################
