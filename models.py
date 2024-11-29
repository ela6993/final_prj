from app import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = 'Users'

    user_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.Text, nullable = False)
    name = db.Column(db.Text, nullable = False)
    password = db.Column(db.Text, nullable = False)
    
    def __repr__(self):
        return f'{self.username} - {self.name}'
    
    def get_id(self):
        return self.user_id
    
class Message(db.Model):
    _tablename__ = 'Chat_messages'

    message_id = db.Column(db.Integer, primary_key = True)
    message_content = db.Column(db.Text, nullable = False)
    chat_id = db.Column(db.Text, nullable = False)
    username = db.Column(db.Text, nullable = False)
    messages_time = db.Column(db.DateTime, default = datetime.utcnow)
