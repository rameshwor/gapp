import webapp2

from apiclient.discovery import build
from oauth2client.appengine import OAuth2Decorator

import settings

decorator = OAuth2Decorator(client_id=settings.CLIENT_ID,
                            client_secret=settings.CLIENT_SECRET,
                            scope=settings.SCOPE)
service = build('tasks', 'v1')

class MainHandler(webapp2.RequestHandler):

   @decorator.oauth_required
   def get(self):
     tasks = service.tasks().list(tasklist='@default').execute(
         http=decorator.http())
     self.response.write('<html><body><ul>')
     for task in tasks['items']:
       self.response.write('<li>%s</li>' % task['title'])
     self.response.write('</ul></body><html>')

application = webapp2.WSGIApplication([
    ('/', MainHandler),
    (decorator.callback_path, decorator.callback_handler()),
    ], debug=True)
