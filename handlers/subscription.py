from handlers.base import BaseHandler
from google.appengine.api import users, memcache
import uuid
from utils.decorators import validate_csrf
from models.subscription import Subscription
from models.topic import Topic


class SubscriptionHandler(BaseHandler):

    @validate_csrf
    def post(self, topic_id):
        topic = Topic.get_by_id(int(topic_id))
        user = users.get_current_user()

        Subscription.create_sub_or_resub(topic=topic, subscriber_email=user.email())

        return self.redirect_to("topic", topic_id=topic.key.id())


class DeleteSubscription(BaseHandler):
    @validate_csrf
    def post(self, topic_id):
        topic = Topic.get_by_id(int(topic_id))
        user = users.get_current_user()

        Subscription.delete_sub(topic=topic, subscriber_email=user.email())

        return self.redirect_to("topic", topic_id=topic.key.id())

