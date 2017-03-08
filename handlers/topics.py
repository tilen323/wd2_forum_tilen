from handlers.base import BaseHandler
from models.topic import Topic
from models.comment import Comment
from models.user import User
from google.appengine.api import users, memcache
import uuid



class TopicCreateHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        csrf_token = str(uuid.uuid4())  # convert UUID to string
        if user:
            memcache.add(key=csrf_token, value=user.email(), time=600)

        params = {"csrf_token": csrf_token}

        return self.render_template("topic_create.html", params=params)
    def post(self):

        user = users.get_current_user()
        if not user:
            return self.write("you are not loged in!")

        csrf_token = self.request.get("csrf_token")
        mem_token = memcache.get(key=csrf_token)

        if not mem_token or str(mem_token) != user.email():
            return self.write("You are evil attacker...")

        title = self.request.get("title")
        content = self.request.get("content")
        author = User.query(User.email == user.email()).fetch()
        author_email = author[0].email
        author_avatar = author[0].avatar_url

        new_topic = Topic(title=title, content=content, author_email=author_email, author_avatar=author_avatar)
        new_topic.put()

        return self.redirect_to("topic", topic_id=new_topic.key.id())

class TopicHandler(BaseHandler):
    def get(self, topic_id):
        user = users.get_current_user()
        csrf_token = str(uuid.uuid4())  # convert UUID to string
        if user:
            memcache.add(key=csrf_token, value=user.email(), time=600)

        topic = Topic.get_by_id(int(topic_id))

        comments = Comment.query(Comment.topic_id == topic.key.id(), Comment.deleted == False).order(Comment.created).fetch()

        params = {"topic": topic, "csrf_token": csrf_token, "comments": comments}

        return self.render_template("topic.html", params=params)

    def post(self, topic_id):
        user = users.get_current_user()
        if not user:
            return self.write("you are not loged in!")

        csrf_token = self.request.get("csrf_token")
        mem_token = memcache.get(key=csrf_token)

        if not mem_token or str(mem_token) != user.email():
            return self.write("You are evil attacker...")

        topic = Topic.get_by_id(int(topic_id))
        comment = self.request.get("content")
        author = User.query(User.email == user.email()).fetch()
        author_email = author[0].email
        author_avatar = author[0].avatar_url

        new_comment = Comment(content=comment, author_email=author_email, topic_title=topic.title, topic_id=topic.key.id(), author_avatar=author_avatar)
        new_comment.put()

        return self.redirect_to("topic", topic_id=topic.key.id())
