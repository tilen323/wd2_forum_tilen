import datetime

from handlers.base import BaseHandler
from models.user import User
from models.topic import Topic
from google.appengine.api import mail


class SubMailSendHandler(BaseHandler):
    def get(self):
        subscribers = User.query(User.forum_subscription == True).fetch()

        latest_topics = Topic.query(Topic.deleted == False,
                                    Topic.updated > datetime.datetime.now() - datetime.timedelta(days=1)).fetch()

        if latest_topics:
            topic_link = ""
            for topic in latest_topics:

                topic_link += topic.title + "- " + "http://wd2-forum-tilen.appspot.com/topic/" + str(topic.key.id()) + " , "

            for subscriber in subscribers:
                mail.send_mail(sender="prevolnik.tilen@gmail.com",
                               to=subscriber.email,
                               subject="Here are the lastest topics from our forum!",
                               body="Topics: %s" % topic_link)