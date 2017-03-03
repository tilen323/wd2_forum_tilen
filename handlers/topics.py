from handlers.base import BaseHandler
from models.topic import Topic
from google.appengine.api import users


class TopicCreateHandler(BaseHandler):
    def get(self):
        return self.render_template("topic_create.html")
    def post(self):
        title = self.request.get("title")
        content = self.request.get("content")

        user = users.get_current_user()
        if not user:
            return self.write("you are not loged in!")

        new_topic = Topic(title=title, content=content, author_email=user.email())
        new_topic.put()

        return self.redirect_to("topic", topic_id=new_topic.key.id())

class TopicHandler(BaseHandler):
    def get(self, topic_id):

        topic = Topic.get_by_id(int(topic_id))

        params = {"topic": topic}

        return self.render_template("topic.html", params=params)