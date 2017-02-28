#!/usr/bin/env python
import os
import jinja2
import webapp2
from handlers.base import MainHandler, AboutHandler, CookieHandler

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name="main-page"),
    webapp2.Route('/about', AboutHandler, name="about-page"),
    webapp2.Route('/set-cookie', CookieHandler, name="nastavi-cookie"),
], debug=True)
