from handlers.base import BaseHandler
from models.topic import Topic
from models.comment import Comment
from models.user import User
from models.subscription import Subscription
from google.appengine.api import users, memcache
import uuid
from utils.decorators import validate_csrf


class TopicCreateHandler(BaseHandler):
    def get(self):

        return self.render_template("topic_create.html")

    @validate_csrf
    def post(self):

        user = users.get_current_user()
        if not user:
            return self.write("you are not loged in!")

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
        topic = Topic.get_by_id(int(topic_id))
        user = users.get_current_user()

        comments = Comment.query(Comment.topic_id == topic.key.id(), Comment.deleted == False).order(Comment.created).fetch()
        comments_sum = len(comments)

        if user:
            subscriber = Subscription.query(Subscription.topic_id == topic.key.id(),
                                            Subscription.deleted == False,
                                            Subscription.subscriber_email == user.email()).get()
        else:
            subscriber = ""

        params = {"topic": topic, "comments": comments, "comments_sum": comments_sum, "user": user, "subscriber": subscriber}

        return self.render_template("topic.html", params=params)

    @validate_csrf
    def post(self, topic_id):
        topic = Topic.get_by_id(int(topic_id))
        user = users.get_current_user()

        if not user:
            return self.write("you are not loged in!")

        comment = self.request.get("content")

        author = User.query(User.email == user.email()).fetch()
        author_email = author[0].email
        author_avatar = author[0].avatar_url

        Comment.create(content=comment, author=author_email, topic=topic, avatar=author_avatar)

        return self.redirect_to("topic", topic_id=topic.key.id())

class EditTopicHandler(BaseHandler):
    def get(self, topic_id):
        topic = Topic.get_by_id(int(topic_id))

        params = {"topic": topic}

        return self.render_template("topic_edit.html", params=params)

    @validate_csrf
    def post(self, topic_id):
        topic = Topic.get_by_id(int(topic_id))
        user = users.get_current_user()

        title = self.request.get("title")
        content = self.request.get("content")

        if user.email() == topic.author_email or users.is_current_user_admin():
            Topic.edit(topic=topic, title=title, content=content)

        return self.redirect_to("topic", topic_id=topic.key.id())

class DeleteTopicHandler(BaseHandler):
    @validate_csrf
    def post(self, topic_id):
        topic = Topic.get_by_id(int(topic_id))
        user = users.get_current_user()

        if user.email() == topic.author_email or users.is_current_user_admin():
            Topic.delete(topic=topic)

        return self.redirect_to("main-page")

