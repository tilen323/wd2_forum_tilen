from handlers.base import BaseHandler
from models.user import User
from models.comment import Comment
from google.appengine.api import users, memcache
import uuid
from utils.decorators import validate_csrf

class UserProfileHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        user_profile = User.query(User.email == user.email()).fetch()
        user_comments = Comment.query(Comment.author_email == user.email()).order(-Comment.created).fetch()
        user_comments_sum = len(user_comments)

        params = {"user_profile": user_profile, "user_comments": user_comments, "user_comments_sum": user_comments_sum}

        return self.render_template("user_profile.html", params=params)


class EditProfileHandler(BaseHandler):
    def get(self, user_id):

        user_profile = User.get_by_id(int(user_id))

        params = {"user_profile": user_profile}

        return self.render_template("user_edit.html", params=params)

    @validate_csrf
    def post(self, user_id):
        user_profile = User.get_by_id(int(user_id))
        first_name = self.request.get("first_name")
        last_name = self.request.get("last_name")
        avatar_url = self.request.get("avatar_url")

        User.edit_profile(user_profile=user_profile, first_name=first_name, last_name=last_name, avatar_url=avatar_url)

        return self.redirect_to("user-profile")

