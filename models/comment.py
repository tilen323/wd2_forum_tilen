from google.appengine.ext import ndb
from google.appengine.api import mail
from google.appengine.api import taskqueue

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

        return new_comment
