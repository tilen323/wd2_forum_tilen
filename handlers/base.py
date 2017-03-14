import os
import jinja2
import webapp2
from google.appengine.api import users
from google.appengine.api import memcache
import uuid
from models.topic import Topic
from models.user import User

template_dir = os.path.join(os.path.dirname(__file__), "../templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}

        # cookies
        cookie = self.request.cookies.get("ninja-cookie")

        if cookie:
            params["piskotki"] = True

        # google login
        user = users.get_current_user()
        if user:
            if users.is_current_user_admin():
                user_admin = True
                params["user_admin"] = user_admin
            params["user"] = User.get_or_create(user.email())
            params["logout_url"] = users.create_logout_url("/")
        else:
            params["login_url"] = users.create_login_url("/")

        csrf_token = str(uuid.uuid4())  # convert UUID to string
        memcache.add(key=csrf_token, value=True, time=600)
        params["csrf_token"] = csrf_token

        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        topic_list = Topic.query(Topic.deleted == False).order(-Topic.created).fetch()

        params = {"topic_list": topic_list}
        return self.render_template("main.html", params=params)


class AboutHandler(BaseHandler):
    def get(self):
        return self.render_template("about.html")

class CookieHandler(BaseHandler):
    def post(self):
        self.response.set_cookie(key="ninja-cookie", value="accepted")
        return self.redirect_to("main-page")