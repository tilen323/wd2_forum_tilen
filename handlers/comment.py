from handlers.base import BaseHandler
from google.appengine.api import users, memcache
from utils.decorators import validate_csrf
from models.comment import Comment


class DeleteCommentHandler(BaseHandler):
    @validate_csrf
    def post(self, comment_id):
        comment = Comment.get_by_id(int(comment_id))

        user = users.get_current_user()

        if user.email() == comment.author_email or users.is_current_user_admin():
            Comment.delete_comment(comment=comment)

        return self.redirect_to("topic", topic_id=comment.topic_id)


