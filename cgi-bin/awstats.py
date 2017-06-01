#!/usr/bin/python
#
# A wrapper around Awstats to restrict config for
# Anchor shared hosting services.
#
# Be sure to edit /etc/awstats/awstats.model.conf and add the line:
#  WrapperScript="./"
#
# NOTE: THIS FILE IS DISTRIBUTED BY CFENGINE. ANY LOCAL CHANGES WILL
#       BE DESTROYED.

import sys, os, cgi, urllib, os.path

# Settings.
AWSTATS_ROOT = '/var/www/awstats'
AWSTATS_BIN = './awstats.pl' 
STATISTICS_ROOT = '/var/www/html/usage'

# Get information from our CGI environment.
try :
	path_translated = os.environ['PATH_TRANSLATED']
	query_string = os.environ['QUERY_STRING']
except KeyError, e :
	print "Content-type: text/plain\n\nEnvironment error"
	sys.stdout.flush()
	sys.exit(1)

# Determine the vhost config to use for Awstats.
path = os.path.abspath(path_translated)
while len(path) > 0 :
	(dirname, basename) = os.path.split(path)
	if dirname == STATISTICS_ROOT :
		vhost = basename
		break
	else :
		path = dirname

# Override config URL parameter.
query = dict ([ (key, val[-1]) for (key, val) in cgi.parse_qs(query_string).items() ])
query['config'] = vhost
os.environ['QUERY_STRING'] = urllib.urlencode(query)

# Run AwStats.
os.chdir(AWSTATS_ROOT)
os.execv(AWSTATS_BIN, ['AWSTATS_BIN'])
