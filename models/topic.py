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
        comment_list = Comment.query(Comment.topic_id == topic.key.id(),
                                     Comment.deleted == False).fetch()

        comment_sum = len(comment_list)

        topic.comment_sum = comment_sum
        topic.put()

        return topic