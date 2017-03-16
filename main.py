#!/usr/bin/env python
import os
import jinja2
import webapp2

from crons.delete_comment_cron import DeleteCommentsCron
from crons.delete_topics_cron import DeleteTopicsCron
from crons.subs_mail_send import SubMailSendHandler
from handlers.base import MainHandler, AboutHandler, CookieHandler
from handlers.comment import DeleteCommentHandler
from handlers.topics import TopicCreateHandler
from handlers.topics import TopicHandler
from handlers.topics import EditTopicHandler
from handlers.topics import DeleteTopicHandler
from handlers.user import EditProfileHandler
from handlers.user import UserProfileHandler
from handlers.subscription import SubscriptionHandler, DeleteSubscriptionHandler, ForumSubscriptionHandler, \
    ForumUnsubscribeHandler
from handlers.admin_test import AdminTestHandler
from workers.email_comment_worker import EmailNewCommentWorker, EmailSubNewCommentWorker

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name="main-page"),
    webapp2.Route('/about', AboutHandler, name="about-page"),
    webapp2.Route('/set-cookie', CookieHandler, name="nastavi-cookie"),
    webapp2.Route('/topic/create', TopicCreateHandler, name="topic_create"),
    webapp2.Route('/topic/<topic_id:\d+>', TopicHandler, name="topic"),
    webapp2.Route('/user/profile', UserProfileHandler, name="user-profile"),
    webapp2.Route('/topic/<topic_id:\d+>/edit', EditTopicHandler, name="edit-topic"),
    webapp2.Route('/topic/<topic_id:\d+>/delete', DeleteTopicHandler, name="delete-topic"),
    webapp2.Route('/admin-test', AdminTestHandler, name="admin-test"),
    webapp2.Route('/profile/<user_id:\d+>/edit', EditProfileHandler, name="edit-profile"),
    webapp2.Route('/add_subscriber/<topic_id:\d+>', SubscriptionHandler),
    webapp2.Route('/delete_subscriber/<topic_id:\d+>', DeleteSubscriptionHandler),
    webapp2.Route('/forum_subscription/<user_id:\d+>', ForumSubscriptionHandler),
    webapp2.Route('/forum_unsubscribe/<user_id:\d+>', ForumUnsubscribeHandler),
    webapp2.Route('/delete_comment/<comment_id:\d+>', DeleteCommentHandler),

    #tasks
    webapp2.Route("/task/email-new-comment", EmailNewCommentWorker),
    webapp2.Route("/task/email-sub-new-comment", EmailSubNewCommentWorker),

    #Cron
    webapp2.Route("/cron/delete-topics", DeleteTopicsCron, name="cron-topics-delete"),
    webapp2.Route("/cron/delete-comments", DeleteCommentsCron, name="cron-comment-delete"),
    webapp2.Route("/cron/subs_mail_send", SubMailSendHandler, name="cron-subs-mail-send"),

], debug=True)
