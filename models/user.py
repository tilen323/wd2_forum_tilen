from google.appengine.ext import ndb

class User(ndb.Model):
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    email = ndb.StringProperty()
    avatar_url = ndb.StringProperty(default="https://s30.postimg.org/6mdag8cip/ninja.png")
    forum_subscription = ndb.BooleanProperty(default=False)
    deleted = ndb.BooleanProperty(default=False)
    admin = ndb.BooleanProperty(default=False)
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)

    @classmethod
    def get_or_create(cls, email):
        user = User.query(User.email == email).get()

        if not user:
            user = User(email=email)
            user.put()

        return user

    @classmethod
    def edit_profile(cls, user_profile, first_name, last_name, avatar_url):

        user_profile.first_name = first_name
        user_profile.last_name = last_name
        user_profile.avatar_url = avatar_url
        user_profile.put()

        return user_profile

    @classmethod
    def subscribe_to_forum(cls, user_profile):

        user_profile.forum_subscription = True
        user_profile.put()

        return user_profile

    @classmethod
    def unsubscribe_from_forum(cls, user_profile):

        user_profile.forum_subscription = False
        user_profile.put()

        return user_profile

    @classmethod
    def set_deleted_false(cls, user_list):

        for profile in user_list:
            profile.deleted = False
            profile.put()

        return user_list
