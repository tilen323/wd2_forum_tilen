from google.appengine.ext import ndb

class Topic(ndb.Model):
    title = ndb.StringProperty()
    content = ndb.StringProperty()
    author_email = ndb.StringProperty()
    author_avatar = ndb.StringProperty()
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