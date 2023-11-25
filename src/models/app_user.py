from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class app_user(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    hashed_password = db.Column(db.Integer, nullable=False)

    def __repr__(self) -> str:
        return f'User({self.user_id}, {self.email}, {self.username}, {self.hashed_password})'