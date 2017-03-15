from handlers.base import BaseHandler
from google.appengine.api import users, memcache
import uuid

from utils.decorators import validate_csrf
from models.subscription import Subscription
from models.topic import Topic
from models.user import User

class SubscriptionHandler(BaseHandler):
    @validate_csrf
    def post(self, topic_id):
        topic = Topic.get_by_id(int(topic_id))
        user = users.get_current_user()

        Subscription.create_sub_or_resub(topic=topic, subscriber_email=user.email())

        return self.redirect_to("topic", topic_id=topic.key.id())


class DeleteSubscriptionHandler(BaseHandler):
    @validate_csrf
    def post(self, topic_id):
        topic = Topic.get_by_id(int(topic_id))
        user = users.get_current_user()

        Subscription.delete_sub(topic=topic, subscriber_email=user.email())

        return self.redirect_to("topic", topic_id=topic.key.id())


class ForumSubscriptionHandler(BaseHandler):
    @validate_csrf
    def post(self, user_id):
        user_profile = User.get_by_id(int(user_id))

        User.subscribe_to_forum(user_profile=user_profile)

        return self.redirect_to("main-page")


class ForumUnsubscribeHandler(BaseHandler):
    @validate_csrf
    def post(self, user_id):
        user_profile = User.get_by_id(int(user_id))

        User.unsubscribe_from_forum(user_profile=user_profile)

        return self.redirect_to("main-page")