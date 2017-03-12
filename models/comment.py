from google.appengine.ext import ndb
from google.appengine.api import mail
from google.appengine.api import taskqueue
from models.subscription import Subscription

class Comment(ndb.Model):
    content = ndb.TextProperty()
    author_email = ndb.StringProperty()
    author_avatar = ndb.StringProperty()
    topic_id = ndb.IntegerProperty()
    topic_title = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    deleted = ndb.BooleanProperty(default=False)

    @classmethod
    def create(cls, content, author, topic, avatar):
        new_comment = Comment(content=content, author_email=author, topic_title=topic.title,
                              topic_id=topic.key.id(), author_avatar=avatar)
        new_comment.put()

        taskqueue.add(url="/task/email-new-comment", params={"topic_author_email": topic.author_email,
                                                             "topic_title": topic.title,
                                                             "comment_content": new_comment.content})

        list_of_subscribers = Subscription.query(Subscription.topic_id == topic.key.id(),
                                                 Subscription.deleted == False).fetch()

        if list_of_subscribers:
            for subscriber in list_of_subscribers:
                taskqueue.add(url="/task/email-sub-new-comment", params={"subscriber_email": subscriber.subscriber_email,
                                                                         "topic_title": topic.title,
                                                                         "comment_content": new_comment.content})

        return new_comment
