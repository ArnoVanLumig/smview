import cherrypy
import os.path
from mako.template import Template
from mako.lookup import TemplateLookup
from test import runAndParse
import sqlite3
import hashlib

current_dir = os.path.dirname(os.path.abspath(__file__))
lookup = TemplateLookup(directories=['templates'])

class SMViewer(object):
	_cp_config = {'tools.staticdir.on' : True,
				  'tools.staticdir.dir' : current_dir + '/static',
	}

	# Create the sqlite database and table
	def setup(self):
		conn = sqlite3.connect('code.db')

		c = conn.cursor()
		c.execute('''DROP TABLE IF EXISTS code;''')
		c.execute('''CREATE TABLE code (hash text, code text, PRIMARY KEY (hash))''')
		conn.commit()

		conn.close()
	setup.exposed = True

	# Just serve the index page
	def index(self):
		tmpl = lookup.get_template("index.html")
		return tmpl.render()
	index.exposed = True

	# Get the code from the database that has the given hash, or empty string otherwise
	def getcode(self, md5):
		conn = sqlite3.connect('code.db')

		c = conn.cursor()
		arg = (md5,)
		c.execute('SELECT code FROM code WHERE hash=?', arg)
		res = c.fetchone()

		if not res:
			res = ""
		else:
			res = res[0]

		conn.close()

		return res
	getcode.exposed = True

	# Run the code in NuSMV and render either the error or success views
	def run(self, code):
		md5 = hashlib.md5(code).hexdigest()

		conn = sqlite3.connect('code.db')
		c = conn.cursor()
		arg = (md5,code,)
		c.execute('INSERT OR IGNORE INTO code (hash, code) VALUES (?, ?)', arg)
		conn.commit()
		conn.close()

		res = runAndParse(code, md5)

		if res[0]:
			tmpl = lookup.get_template("result.html")
			return tmpl.render(result=res[1], md5=md5)
		else:
			tmpl = lookup.get_template("resultError.html")
			return tmpl.render(result=res[1], md5=md5)

	run.exposed = True

cherrypy.config.update({'server.socket_host': '0.0.0.0'} )
cherrypy.quickstart(SMViewer())
