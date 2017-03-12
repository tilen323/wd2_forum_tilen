from google.appengine.ext import ndb

class Subscription(ndb.Model):
    topic_id = ndb.IntegerProperty()
    topic_title = ndb.StringProperty()
    subscriber_email = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    deleted = ndb.BooleanProperty(default=False)

    @classmethod
    def create_sub_or_resub(cls, topic, subscriber_email):

        subscription = Subscription.query(Subscription.subscriber_email == subscriber_email,
                                          Subscription.topic_id == topic.key.id()).get()

        if subscription:
            subscription.deleted = False
            subscription.put()
        else:
            subscription = Subscription(topic_id=topic.key.id(), topic_title=topic.title, subscriber_email=subscriber_email)
            subscription.put()

        return subscription


    @classmethod
    def delete_sub(cls, topic, subscriber_email):
        subscription = Subscription.query(Subscription.subscriber_email == subscriber_email,
                                          Subscription.topic_id == topic.key.id()).get()

        subscription.deleted = True
        subscription.put()

        return subscription