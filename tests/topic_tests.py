import os
import unittest

import webapp2
import webtest

from google.appengine.ext import testbed
from google.appengine.api import users, memcache

import uuid

from handlers.base import MainHandler
from handlers.topics import TopicCreateHandler, TopicHandler, EditTopicHandler, DeleteTopicHandler
from models.topic import Topic


class TopicTests(unittest.TestCase):
    def setUp(self):
        app = webapp2.WSGIApplication(
            [
                webapp2.Route('/topic/create', TopicCreateHandler, name="topic_create"),
                webapp2.Route('/topic/<topic_id:\d+>', TopicHandler, name="topic"),
                webapp2.Route('/topic/<topic_id:\d+>/edit', EditTopicHandler, name="edit-topic"),
                webapp2.Route('/topic/<topic_id:\d+>/delete', DeleteTopicHandler, name="delete-topic"),
                webapp2.Route('/', MainHandler, name="main-page"),
            ])

        self.testapp = webtest.TestApp(app)
        self.testbed = testbed.Testbed()
        self.testbed.activate()

        """ Uncomment the stubs that you need to run tests. """
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        # self.testbed.init_mail_stub()
        # self.testbed.init_taskqueue_stub()
        self.testbed.init_user_stub()
        # ...

        """ Uncomment if you need user (Google Login) and if this user needs to be admin. """
        os.environ['USER_EMAIL'] = 'some.user@example.com'
        # os.environ['USER_IS_ADMIN'] = '1'

    def tearDown(self):
        self.testbed.deactivate()

    def test_add_topic_handler(self):
        # get
        get = self.testapp.get('/topic/create')
        self.assertEqual(get.status_int, 200)

        self.assertIn("Create Topic", get.body)

        # post
        title = "Moj testni topic"
        content = "bla bla bla"
        author_email = "some.user@example.com"
        author_avatar = "https://s30.postimg.org/6mdag8cip/ninja.png"

        csrf_token = str(uuid.uuid4())  # convert UUID to string
        memcache.add(key=csrf_token, value=True, time=600)

        params = {"title": title, "content": content, "author_email": author_email, "author_avatar": author_avatar, "csrf_token": csrf_token}

        post = self.testapp.post("/topic/create", params=params)
        self.assertEqual(post.status_int, 302)

        topic = Topic.query().get()  # get the topic create by this text (it's the only one in this fake database)
        self.assertTrue(topic.title, title)  # check if topic title is the same as we wrote above
        self.assertTrue(topic.content, content)

    def test_topic_details_handler(self):
        # GET
        topic = Topic(title="Another topic", content="Some text in the topic", author_email="some.user@example.com", author_avatar="https://s30.postimg.org/6mdag8cip/ninja.png")
        topic.put()

        get = self.testapp.get('/topic/{}'.format(topic.key.id()))  # do a GET request
        self.assertEqual(get.status_int, 200)

    def test_topic_delete_handler(self):
        # POST
        topic = Topic(title="Topic to delete", content="Some text in the topic",
                      author_email="some.user@example.com")
        topic.put()  # save topic in database

        topic_query_1 = Topic.query().get()
        self.assertTrue(topic_query_1)  # assert that topic exists in a database

        csrf_token = str(uuid.uuid4())  # create a CSRF token
        memcache.add(key=csrf_token, value=True, time=600)  # save token to memcache

        params = {"csrf_token": csrf_token}

        post = self.testapp.post('/topic/{}/delete'.format(topic.key.id()), params)  # do a GET request
        self.assertEqual(post.status_int,
                         302)  # when topic is deleted, handler redirects to main page (302 == redirect)

        topic_query_2 = Topic.query().get()

        self.assertTrue(topic_query_2.deleted)  # assert that "deleted" field is set to True


