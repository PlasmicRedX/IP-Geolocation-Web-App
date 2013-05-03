import sys, string, GeoIP

location = ""
myfile = None
## creating an object
myGeoIP = GeoIP.new(GeoIP.GEOIP_STANDARD)

## Using GeoIP Memory Cache
myGeoIP = GeoIP.new(GeoIP.GEOIP_MEMORY_CACHE | GeoIP.GEOIP_CHECK_CACHE)

try:
	myfile = open('/home/redx/myipaddrs.txt','r')
	## using the City database
	myGeoIP=GeoIP.open("GeoLiteCity.dat",GeoIP.GEOIP_STANDARD)

except Exception:
	print "Uh Oh, Spaghettios! Can not open the file!"
	raise

for line in myfile.readlines():
	words = string.split(line)
	if len(words) >= 2:
		geoRecord = myGeoIP.record_by_addr(words[0])
		if geoRecord!= None:
			location = location + str(geoRecord ['latitude']) + " " + str(geoRecord ['longitude']) + " "
	else:
		print "Invalid line detected. Only one word on this line!"
print location.split(" ")
print "the location is %s" % location
myfile.close()
