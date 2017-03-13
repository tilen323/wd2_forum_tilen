from handlers.base import BaseHandler
from google.appengine.api import mail

class EmailNewCommentWorker(BaseHandler):
    def post(self):

        topic_author_email = self.request.get("topic_author_email")
        topic_title = self.request.get("topic_title")
        comment_content = self.request.get("comment_content")

        mail.send_mail(sender="prevolnik.tilen@gmail.com",
                       to=topic_author_email,
                       subject="Dobil si nov komentar v topicu %s!" % topic_title,
                       body="Nov komentar: {}".format(comment_content))


class EmailSubNewCommentWorker(BaseHandler):
    def post(self):

        subscriber_email = self.request.get("subscriber_email")
        topic_title = self.request.get("topic_title")
        comment_content = self.request.get("comment_content")

        mail.send_mail(sender="prevolnik.tilen@gmail.com",
                       to=subscriber_email,
                       subject="Dobil si nov komentar v topicu %s, na katerega si narocen!" % topic_title,
                       body="Nov komentar: {}".format(comment_content))