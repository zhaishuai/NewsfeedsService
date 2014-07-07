from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('newsfeedsDataLayer.views',
    url('creatUser/$','creatUser'),
    url('recommendation?$','recommendation'),
    url('readArtical?$','readArtical'),
    url('getUserKeyWord?$','getUserKeyWord'),
    url('getArticalByKind?$','getArticalByKind'),
    url('readRelatedArtical?$','readRelatedArtical'),
    url("getHtml?$","getHtml")
    # Examples:
    # url(r'^$', 'testNewsfeeds.views.home', name='home'),
    # url(r'^testNewsfeeds/', include('testNewsfeeds.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

urlpatterns = format_suffix_patterns(urlpatterns)