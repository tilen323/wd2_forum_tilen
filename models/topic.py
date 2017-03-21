from google.appengine.ext import ndb
from models.comment import Comment

class Topic(ndb.Model):
    title = ndb.StringProperty()
    content = ndb.StringProperty()
    author_email = ndb.StringProperty()
    author_avatar = ndb.StringProperty()
    comment_sum = ndb.IntegerProperty(default=0)
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    deleted = ndb.BooleanProperty(default=False)

    @classmethod
    def add_topic(cls, title, content, author_email, author_avatar):
        new_topic = Topic(title=title, content=content, author_email=author_email, author_avatar=author_avatar)
        new_topic.put()
        return new_topic

    @classmethod
    def edit(cls, topic, title, content):
        topic.title = title
        topic.content = content
        topic.put()
        return topic

    @classmethod
    def delete(cls, topic):
        topic.deleted = True
        topic.put()
        return topic

    @classmethod
    def comment_sum_add(cls, topic):
        topic.comment_sum += 1
        topic.put()
        return topic

    @classmethod
    def comment_sum_minus_one(cls, topic):
        topic.comment_sum -= 1
        topic.put()
        return topic