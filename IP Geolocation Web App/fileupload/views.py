# encoding: utf-8

import os, sys, string, GeoIP

from fileupload.models import Picture
from django.views.generic import CreateView, DeleteView

from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from django.core.urlresolvers import reverse

from django.conf import settings

def response_mimetype(request):
    if "application/json" in request.META['HTTP_ACCEPT']:
        return "application/json"
    else:
        return "text/plain"

class PictureCreateView(CreateView):
    model = Picture

    def form_valid(self, form):
        self.object = form.save()
        f = self.request.FILES.get('file')
        data = [{'name': f.name, 'url': settings.MEDIA_URL + "pictures/" + f.name.replace(" ", "_"), 'thumbnail_url': settings.MEDIA_URL + "pictures/" + f.name.replace(" ", "_"), 'delete_url': reverse('upload-delete', args=[self.object.id]), 'delete_type': "DELETE"}]
        response = JSONResponse(data, {}, response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response

    def get_context_data(self, **kwargs):
        context = super(PictureCreateView, self).get_context_data(**kwargs)
        context['pictures'] = Picture.objects.all()
        return context


class PictureDeleteView(DeleteView):
    model = Picture

    def delete(self, request, *args, **kwargs):
	"""
	This does not actually delete the file, only the database record.  But
	that is easy to implement.
	"""
	self.object = self.get_object()
	location = ""
	ipAddrs = ""
	conCat = ""
	myfile = None
	fn = os.getcwd() +  settings.MEDIA_URL + self.object.file.name.replace(" ", "_")
	print fn
	## creating an object
	myGeoIP = GeoIP.new(GeoIP.GEOIP_STANDARD)

	## Using GeoIP Memory Cache
	myGeoIP = GeoIP.new(GeoIP.GEOIP_MEMORY_CACHE | GeoIP.GEOIP_CHECK_CACHE)

	## using the City database
	myGeoIP=GeoIP.open("GeoLiteCity.dat",GeoIP.GEOIP_STANDARD)

	try:
		myfile = open(fn,'r')
	except Exception:
		print "Uh Oh, Spaghettios! Can not open the file!"
		raise

	for line in myfile.readlines():
		words = string.split(line)
		if len(words) >= 2:
			geoRecord = myGeoIP.record_by_addr(words[0])
			if geoRecord!= None:
				location = location + str(geoRecord ['latitude']) + " " + str(geoRecord ['longitude']) + " "
				ipAddrs = ipAddrs + ''.join(words[0]) + " "
		else:
			print "Invalid line detected. Only one word on this line!"
	print ipAddrs
	myfile.close()
	self.object.delete()
	return HttpResponse('''<!DOCTYPE html>
<html>
  <head>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
    <style type="text/css">
      html {{ height: 100% }}
      body {{ height: 100%; margin: 0; padding: 0 }}
      #map-canvas {{ height: 100% }}
    </style>
    <script type="text/javascript"
      src="https://maps.googleapis.com/maps/api/js?key=AIzaSyAp5Ma-hrUk6iuOrd58hg2jngG9gjRPm- g&sensor=false">
    </script>
    <title>IP Geolocations</title>
    <script type="text/javascript">
	<!--var temp = "39.9612007141 -82.9988021851 31.527299881 -110.360702515 30.5800991058 114.273399353 39.9612007141 82.9988021851 ";-->
	var temp = "{1}";
	var i = 0;
	var count1 = 0;
	var count2 = 0;
	temp = temp.substring(0, temp.length - 1);
	tempArray = new Array();
	tempArray = temp.split(" ");
	tempArray1 = new Array();
	locationNameArray = new Array();
	var cool = "";
	
	locationArray = new Array();
		
	for (var i=0; i < tempArray.length; i+=2) {{
		cool = tempArray[i] + "," + tempArray[i+1];
    		locationArray[count1] = cool.split(",");
		count1++;
    }}
	<!-- var temp1 = "11.24.3.4 55.23.47.18 27.18.222.34 22.54.123.78"; -->
		var temp1 = "{2}";
	tempArray1 = temp1.split(' ');
	for (i=0; i < tempArray1.length; i++) {{
		cool = tempArray1[i];
    	locationNameArray[count2] = cool;
		count2++;
    }}
      function initialize() {{
        var mapOptions = {{
          center: new google.maps.LatLng(0, 0),
          zoom: 2,
          mapTypeId: google.maps.MapTypeId.ROADMAP
        }}
        var map = new google.maps.Map(document.getElementById("map-canvas"),
            mapOptions);
	var j = 0;
		for (i=0; i< tempArray.length/2; i++) {{
			for (j=0; j < 1; j++){{
				new google.maps.Marker({{
				position: new google.maps.LatLng(locationArray[i][j],  locationArray[i][j+1]),
				map: map,
				title: locationNameArray[i]
                }})
            }}
        }}
      }}
      google.maps.event.addDomListener(window, 'load', initialize);
    </script>
  </head>
  <body>
    {0} {3} <!-- Here is where the format string (passme) will show up-->
    <div id="map-canvas"/>
  </body>
</html>
'''.format('<h1>IP Geolocation Map</h1>', location, ipAddrs, '<a href=127.0.0.1:8000/upload/new/>Go Back Home</a>'))
	#self.object.delete()
	#if request.is_ajax():
		#response = JSONResponse(True, {}, response_mimetype(self.request))
		#response['Content-Disposition'] = 'inline; filename=files.json'
		#return response
	#else:
		#return HttpResponseRedirect('/upload/new')
        

class JSONResponse(HttpResponse):
    """JSON response class."""
    def __init__(self,obj='',json_opts={},mimetype="application/json",*args,**kwargs):
        content = simplejson.dumps(obj,**json_opts)
        super(JSONResponse,self).__init__(content,mimetype,*args,**kwargs)
