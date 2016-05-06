#!/usr/bin/python
import cgi
import os
import cgitb
import sqlite3
from   geopy.geocoders import Nominatim
conn=sqlite3.connect(r'/nfs/OGN/DIRdata/OGN.db')
curs=conn.cursor()
curs2=conn.cursor()

cgitb.enable()

#                    select count(*), max(altitude), max(distance) from OGNDATA where idflarm = 'DDE48A' and date = '260815' ;
form=cgi.FieldStorage()
print("Content-type: text/html\n")

html1="""<head><meta charset="UTF-8"></head><TITLE>Get the flights</TITLE> <IMG src="../gif/ogn-logo-150x150.png" border=1 alt=[image]><H1>The flights for the selected date are: </H1> <HR> <P> %s </P> </HR> """
#html1="""<TITLE>Get the flights</TITLE> <H1>The OGN flights for the selected date are: </H1> <HR> <P> %s </P> </HR> """
html2="""<center><table><tr><td><pre>"""
html3="""</pre></td></tr></table></center>"""
html4='<a href="http://cunimb.net/igc2map.php?lien=http://repoogn.ddns.net:50080/DIRdata/fd/'

rootdir = "/nfs/OGN/DIRdata/fd"
nlines=0

if not 'dd' in form:
	print (html1 % 'Invalid date')
else:
	dd=form['dd'].value
	mm=form['mm'].value
	yy=form['yy'].value
	if int(dd) > 0 and int(dd) <32 and int(mm) > 0 and int(mm) < 13 and int(yy) > 14 and int(yy) < 18:
		vd = ('Valid date: %s-%s-%s. </br>Select now the flight to display:' %(dd, mm, yy))
	else:
		vd = "Invalid date ..."
	print (html1 % vd)
	print html2
	dir=rootdir+'/Y'+yy+'/M'+mm
	ld=os.listdir(dir)
	for f in ld:
		if f[0:2] == "FD" and f[2:4] == yy and f[4:6] == mm and f[6:8] == dd:
			id=f[-10:-4]
			dte=yy+mm+dd
                    	curs.execute("select count(*), max(altitude), max(distance) from OGNDATA where idflarm = ? and date = ? ", (id, dte))
			reg=curs.fetchone()
			if reg and reg != None:
				cnt=reg[0]
				if cnt == None: cnt=0
				alt=reg[1]
				if alt == None: alt=0.0
				dst=reg[2]
				if dst == None: dst=0.0
                                geolocator = Nominatim(timeout=20)
                                curs.execute("select max(altitude), latitude, longitude from OGNDATA where idflarm = ? and date = ? ", (id, dte))
                                reg=curs.fetchone()
                                if reg and reg != None:
                                        malt=reg[0]
                                        if malt == alt:
                                                lati=reg[1]
                                                long=reg[2]
                                                #loc = geolocator.reverse([lati,long])
                                                #addr=(loc.address).encode('utf8')
						addr=' '
                                        else:
                                                lati=0.0
                                                long=0.0
                                                addr=''
	    		else:
				cnt=0
				alt=0.0
				dst=0.0
                                addr=''
                                lati=0.0
                                long=0.0
			nlines += 1
			details =  (" ==> Count(%4d) MDist(%5.1f) MAlt(%6.1f) Lat(%7.4f) Long(%7.4f) %s " % (cnt, dst, alt, lati, long, addr))
			fn=html4 + 'Y' + yy + '/M' + mm + '/' + f.lstrip()
			fname=("FN:%-33s" % f)
			print fn , '">MAP</a>', "<a>", fname, details,  "</a>"
	if nlines == 0:
		print "No flights found"
	print html3
	

