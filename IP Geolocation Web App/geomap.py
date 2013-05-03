import GeoIP

## creating an object
myGeoIP = GeoIP.new(GeoIP.GEOIP_STANDARD)

 
print myGeoIP.country_code_by_addr("193.45.25.158")
print myGeoIP.country_code_by_name("codemiles.com")

 
## Using GeoIP Memory Cache
myGeoIP = GeoIP.new(GeoIP.GEOIP_MEMORY_CACHE | GeoIP.GEOIP_CHECK_CACHE)
 
print myGeoIP.country_code_by_addr("173.15.27.167")
print myGeoIP.country_code_by_name("codemiles.com")

## using the City database
myGeoIP=GeoIP.open("GeoLiteCity.dat",GeoIP.GEOIP_STANDARD)

print "Using GeoIP City database"
geoRecord = myGeoIP.record_by_addr("173.15.27.167")

if geoRecord!= None:
    print geoRecord ['country_code']
    print geoRecord ['country_name']
    print geoRecord ['time_zone']
    print geoRecord ['city']
    print geoRecord ['region']
    print geoRecord ['region_name']
    print geoRecord ['postal_code']
    print geoRecord ['latitude']
    print geoRecord ['longitude']
    print geoRecord ['area_code']
