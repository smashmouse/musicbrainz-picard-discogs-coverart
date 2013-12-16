#
# Plugin to get the coverart images from Discogs
#
PLUGIN_NAME = 'Discogs Cover Art Downloader'
PLUGIN_AUTHOR = 'Paul Wilson'
PLUGIN_DESCRIPTION = '''Downloads cover artwork for releases that have a Discogs URL.'''
PLUGIN_VERSION = "0.0.5"
PLUGIN_API_VERSIONS = ["1.2"]


from picard.metadata import register_album_metadata_processor
from picard import log
import re
import urllib2
import json


#
# The Discogs API release resource will be set to the value of the 
# release id obtained from the discogs relation.
#
DISCOGS_API_URL = 'http://api.discogs.com/release/'
#
# Discogs will return 500 error if a user agent isn't sent in the HTTP request
#
DISCOGS_USER_AGENT = "MusicBrainzDiscogsCoverartPlugin/" + PLUGIN_VERSION
	
def get_discogs_cover(album, metadata, release):
#
# Try and find a Discogs relationship.  If so, pass the Discogs URL to _process_discogs_relation function
#
	if release.children.has_key('relation_list'):
		for relation_list in release.relation_list:
			if relation_list.target_type == 'url':
				for relation in relation_list.relation:
					if relation.type == 'discogs':
						_process_discogs_relation(relation.target[0].text)

	
	
def _process_discogs_relation(dcurl):
#
# Once this function is called with the discogs url, it will get the discogs image url
#
	log.error ("discogs relation is: %s", dcurl)

	slashindex = dcurl.rfind('/')
	dcrelease = dcurl[slashindex+1:len(dcurl)]

	_process_discogs_release(dcrelease)

	
def _process_discogs_release(dcrelease):
	
	log.error ("discogs release id is: %s", dcrelease)
  
	dcapiurl = DISCOGS_API_URL + dcrelease

	request = urllib2.Request(dcapiurl)
	request.add_header('User-Agent',DISCOGS_USER_AGENT)

	response = urllib2.urlopen(request)
	
	dcreleaseresource = response.read()
	dcapiresp = json.loads(dcreleaseresource)

	dcimages = dcapiresp['resp']['release']['images']

	for dcimg in dcimages:
		if dcimg['type'] == 'primary':
			log.error(dcimg['resource_url'])


	response.close()


register_album_metadata_processor(get_discogs_cover)