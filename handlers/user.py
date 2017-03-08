from handlers.base import BaseHandler
from models.user import User
from google.appengine.api import users, memcache
import uuid

class UserProfileHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        user_profile = User.query(User.email == user.email()).fetch()

        params = {"user_profile": user_profile}

        return self.render_template("user_profile.html", params=params)
