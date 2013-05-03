from django.conf.urls.defaults import *
from django.conf.urls import url
from fileupload.views import PictureCreateView, PictureDeleteView

# urlpatterns = patterns('',
#     (r'^new/$', PictureCreateView.as_view(), {}, 'upload-new'),
#     (r'^delete/(?P<pk>\d+)$', PictureDeleteView.as_view(), {}, 'upload-delete'),
# )
urlpatterns = patterns('',
    url(r'^new/$', PictureCreateView.as_view(), name="upload-new"),
    url(r'^map/(?P<pk>\d+)$', PictureDeleteView.as_view(), name="upload-map"),
    url(r'^delete/(?P<pk>\d+)$', PictureDeleteView.as_view(), name="upload-delete"),
)

