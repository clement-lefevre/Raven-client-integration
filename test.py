#!/home/clement/9h37/sentry/.venv/bin/python
#-*- coding:utf-8 -*-

from raven import Client

client = Client(dsn='http://3d08ecd85ea34e9f9b9c3f8bc0b7f3bb:3ad1a690332f46028a289173efe8412d@localhost:9000/1')

#client = Client(
#	servers=['http://localhost:9000'],
#	project=1,
#	public_key='3d08ecd85ea34e9f9b9c3f8bc0b7f3bb',
#	secret_key='3ad1a690332f46028a289173efe8412d'
#)

client.captureMessage('hello world!')

try:
	1/0
except ZeroDivisionError:
	ident = client.get_ident(client.captureException())
	print "Exception caught; reference is {0}".format(ident)

