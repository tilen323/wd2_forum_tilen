import os
import unittest

import webapp2
import webtest

from google.appengine.ext import testbed
from google.appengine.api import users, memcache

import uuid

from models.user import User
from models.comment import Comment
from models.topic import Topic

from handlers.base import MainHandler
from handlers.user import UserProfileHandler, EditProfileHandler


class CommentTests(unittest.TestCase):
    def setUp(self):
        app = webapp2.WSGIApplication(
            [
                webapp2.Route('/user/profile', UserProfileHandler, name="user-profile"),
                webapp2.Route('/profile/<user_id:\d+>/edit', EditProfileHandler, name="edit-profile"),
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

    def test_user_profile(self):
        #GET
        get = self.testapp.get('/user/profile')
        self.assertEqual(get.status_int, 200)

        self.assertIn("My Profile", get.body)

    def test_edit_profile(self):
        #GET
        user = User(first_name="test", last_name="testek", email="some.user@example.com",
                    avatar_url="https://s30.postimg.org/6mdag8cip/ninja.png")
        user.put()
        user_profile = User.query().get()
        self.assertTrue(user_profile)

        get = self.testapp.get('/profile/{}/edit'.format(user_profile.key.id()))
        self.assertEqual(get.status_int, 200)

        #POST
        user = User(first_name="test", last_name="testek", email="some.user@example.com",
                    avatar_url="https://s30.postimg.org/6mdag8cip/ninja.png")
        user.put()
        user_profile = User.query().get()
        first_name = "janez"
        last_name = "novak"
        avatar_url = "https://s30.postimg.org/6mdag8cip/ninja.png"

        csrf_token = str(uuid.uuid4())  # convert UUID to string
        memcache.add(key=csrf_token, value=True, time=600)

        params = {"user_profile": user_profile, "first_name": first_name, "last_name": last_name, "avatar_url": avatar_url,
                  "csrf_token": csrf_token}

        post = self.testapp.post('/profile/{}/edit'.format(user_profile.key.id()), params=params)
        self.assertEqual(post.status_int, 302)

        user_query = User.query().get()
        self.assertTrue(user_query.first_name, first_name)




