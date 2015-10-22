#!/usr/bin/python

import time
from bs4 import BeautifulSoup as parser
import requests
import sys, os
import sqlite3

newdb = False
if not os.path.exists('wiki.db'):
	newdb = True

conn = sqlite3.connect('wiki.db')
if newdb:
	c = conn.cursor()
	c.execute('CREATE TABLE connections (start text, fin text)')
	conn.commit()

nexturl = ''
if len(sys.argv) == 2:
	nexturl = "http://en.wikipedia.org/wiki/" + sys.argv[1]
else:
	nexturl = "http://en.wikipedia.org/wiki/Special:Random"

bodyhref = ""
lasttopic = ""

esc = False
while not esc:
	try:
		c = conn.cursor()
		req = requests.get(nexturl, headers={'User-Agent' : "Magic Browser"})
		txt = req.text
		dat = parser(txt,"lxml")
		if lasttopic == '':
			lasttopic = dat.title.string.replace(' - Wikipedia, the free encyclopedia','')
		bodytext = dat.body.find('div', attrs={'id':'content'}).find('div', attrs={'id':'bodyContent'}).find('div', attrs={'id':'mw-content-text'})
		hrefs = []
		for i in bodytext.find_all('p'):
			for j in i.find_all('a'):
				hrefs.append(j.get('href'))
		#print hrefs
		for i in hrefs:
			if '/wiki/' in i and not ':' in i and not '#' in i and i != '':
				bodyhref = i
				break
		b = bodyhref.split('/')[-1].replace('_',' ')
		print b
		c.execute('INSERT INTO connections VALUES (?,?)',(lasttopic,b))
		nexturl = 'http://en.wikipedia.org' + bodyhref
		if b == "Philosophy":
			print "Got to Philosophy!"
			nexturl = "http://en.wikipedia.org/wiki/Special:Random"
			lasttopic = ''
			#esc = True
		c.execute('SELECT * FROM connections WHERE fin=?',(b,))
		c.execute('SELECT * FROM connections WHERE start=?',(b,))
		if len(c.fetchall()) > 0:
			print "Infinite loop!"
			nexturl = "http://en.wikipedia.org/wiki/Special:Random"
			lasttopic = ''
			#esc = True
		conn.commit()
		if lasttopic != '':
			lasttopic = b
		time.sleep(1)
	except KeyboardInterrupt:
		print 'exiting......'
		esc = True

conn.close()
