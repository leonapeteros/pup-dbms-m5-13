import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
import jinja2
import os
import urllib
import logging
import json



JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class Thesis(ndb.Model):
	thesis_year = ndb.StringProperty(indexed=True)
	thesis_title = ndb.StringProperty(indexed=True)
	thesis_abstract = ndb.StringProperty(indexed=True)
	thesis_adviser = ndb.StringProperty(indexed=True)
	thesis_section = ndb.StringProperty(indexed=True)
	thesis_createdby = ndb.StringProperty(indexed=True)
	date = ndb.DateTimeProperty(auto_now_add=True)

class User(ndb.Model):
	first_name = ndb.StringProperty(indexed=True)
	last_name = ndb.StringProperty(indexed=True)
	contact_number = ndb.StringProperty(indexed=True)
	user_id = ndb.StringProperty(indexed=True)
	email = ndb.StringProperty(indexed=True)
	date = ndb.DateTimeProperty(auto_now_add=True)


class MainPageHandler(webapp2.RequestHandler):
    def get(self):
    	user_logged_in = users.get_current_user()

    	if user_logged_in:
    		user = User(id = user_logged_in.user_id(), email = user_logged_in.email())
    		user_key = ndb.Key('User', user_logged_in.user_id())
    		user = user_key.get()

    		if user:
	    		url = users.create_logout_url(self.request.uri)
	    		url_linktext = 'Logout'

	    		template_values = {
	    			'user': user_logged_in,
	    			'url': url,
	    			'url_linktext': url_linktext
	    		}

	    		template = JINJA_ENVIRONMENT.get_template('main.html')
	    		self.response.write(template.render(template_values))
	    	else:
	    		self.redirect('/api/user')
    	else:
    		self.redirect('/login')

class APIThesis(webapp2.RequestHandler):
	def get(self):
		thesis = Thesis.query().order(-Thesis.date).fetch()
		thesis_list = []
		user_logged_in = users.get_current_user()

		for entry in thesis:
			thesis_list.append({
				'id': entry.key.id(),
				'thesis_year': entry.thesis_year,
				'thesis_title': entry.thesis_title,
				'thesis_abstract': entry.thesis_abstract,
				'thesis_adviser': entry.thesis_adviser,
				'thesis_section': entry.thesis_section,
				'thesis_createdby': entry.thesis_createdby
			})

		response = {
        	'result': 'OK',
        	'data': thesis_list
        }

	        self.response.headers['Content-Type'] = 'application/json'
	        self.response.out.write(json.dumps(response))

	def post(self):
		thesis = Thesis()
		user_logged_in = users.get_current_user()

		thesis.thesis_year = self.request.get('thesis_year')
		thesis.thesis_title = self.request.get('thesis_title')
		thesis.thesis_abstract = self.request.get('thesis_abstract')
		thesis.thesis_adviser = self.request.get('thesis_adviser')
		thesis.thesis_section = self.request.get('thesis_section')
		thesis.thesis_createdby = user_logged_in.email()
		thesis.put()

		self.response.headers['Content-Type'] = 'application/json'
		response = {
		    'result': 'OK',
		        'data': {
		            'id': thesis.key.id(),
		            'thesis_year': thesis.thesis_year,
		            'thesis_title': thesis.thesis_title,
		            'thesis_abstract': thesis.thesis_abstract,
		            'thesis_adviser': thesis.thesis_adviser,
		            'thesis_section': thesis.thesis_section,
		            'thesis_createdby': thesis.thesis_createdby,
		        }
		}
		self.response.out.write(json.dumps(response))

class loginPage(webapp2.RequestHandler):
	def get(self):
		user_logged_in = users.get_current_user()

		if user_logged_in:
			self.redirect('/')
		else:
			url = users.create_login_url('/api/user')
			url_linktext = "Login"

			template_values = {
				'url': url,
				'url_linktext': url_linktext
			}

			template = JINJA_ENVIRONMENT.get_template('login.html')
			self.response.write(template.render(template_values))

class registerPage(webapp2.RequestHandler):
	def get(self):
		user_logged_in = users.get_current_user()

		if user_logged_in:
			user_key = ndb.Key('User', user_logged_in.user_id())
			user = user_key.get()

			if user:
				self.redirect('/')
			else:
				url = users.create_logout_url('/login')
				url_linktext = "Logout"

				template_values = {
					'url': url,
					'url_linktext': url_linktext
				}

				template = JINJA_ENVIRONMENT.get_template('register.html')
				self.response.write(template.render(template_values))
		else:
			self.redirect(users.create_login_url(self.request.uri))

	def post(self):
		user_logged_in = users.get_current_user()
		user = User(id = user_logged_in.user_id(), email = user_logged_in.email())

		user.first_name = self.request.get('first_name')
		user.last_name = self.request.get('last_name')
		user.contact_number = self.request.get('contact_number')
		user.user_id = user_logged_in.user_id()
		user.put()

		self.response.headers['Content-Type'] = 'application/json'
		response = {
			'result': 'OK',
			'data': {
				'first_name': user.first_name,
				'last_name': user.last_name,
				'contact_number': user.contact_number,
				'user_id': user.user_id,
				'email': user.email
			}
		}

		self.response.out.write(json.dumps(response))

class deleteThesis(webapp2.RequestHandler):
	def get(self, thesis_id):
		thesis = Thesis.get_by_id(int(thesis_id))
		thesis.key.delete()
		self.redirect('/')

class editThesis(webapp2.RequestHandler):
	def get(self, thesis_id):
		thesis = Thesis.get_by_id(int(thesis_id))
		template_values = {
			'thesis': thesis
		}	
		template = JINJA_ENVIRONMENT.get_template('edit.html')
		self.response.write(template.render(template_values))

	def post(self, thesis_id):
		user_logged_in = users.get_current_user()
		thesis = Thesis.get_by_id(int(thesis_id))
		thesis.thesis_year = self.request.get('thesis_year')
		thesis.thesis_title = self.request.get('thesis_title')
		thesis.thesis_abstract = self.request.get('thesis_abstract')
		thesis.thesis_adviser = self.request.get('thesis_adviser')
		thesis.thesis_section = self.request.get('thesis_section')
		thesis.thesis_createdby = user_logged_in.email()
		thesis.put()
		self.redirect('/')

app = webapp2.WSGIApplication([
    ('/home', MainPageHandler),
    ('/', MainPageHandler),
    ('/api/thesis', APIThesis),
    ('/login', loginPage),
    ('/api/user', registerPage),
    ('/delete/(.*)', deleteThesis),
    ('/edit/(.*)', editThesis)
], debug=True)