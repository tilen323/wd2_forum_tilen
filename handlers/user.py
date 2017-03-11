from handlers.base import BaseHandler
from models.user import User
from models.comment import Comment
from google.appengine.api import users, memcache
import uuid

class UserProfileHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        user_profile = User.query(User.email == user.email()).fetch()
        user_comments = Comment.query(Comment.author_email == user.email()).order(-Comment.created).fetch()
        user_comments_sum = len(user_comments)

        params = {"user_profile": user_profile, "user_comments": user_comments, "user_comments_sum": user_comments_sum}

        return self.render_template("user_profile.html", params=params)
