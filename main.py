#!/usr/bin/env python
import os
import jinja2
import webapp2
from handlers.base import MainHandler, AboutHandler, CookieHandler
from handlers.topics import TopicCreateHandler
from handlers.topics import TopicHandler
from handlers.topics import EditTopicHandler
from handlers.user import UserProfileHandler
from workers.email_comment_worker import EmailNewCommentWorker

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name="main-page"),
    webapp2.Route('/about', AboutHandler, name="about-page"),
    webapp2.Route('/set-cookie', CookieHandler, name="nastavi-cookie"),
    webapp2.Route('/topic/create', TopicCreateHandler, name="topic_create"),
    webapp2.Route('/topic/<topic_id:\d+>', TopicHandler, name="topic"),
    webapp2.Route('/user/profile', UserProfileHandler, name="user-profile"),
    webapp2.Route('/topic/<topic_id:\d+>/edit', EditTopicHandler),

    #tasks
    webapp2.Route("/task/email-new-comment", EmailNewCommentWorker)
], debug=True)
