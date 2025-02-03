from App.extensions import db

class User(db.Model):
    # x用户
    x_id = db.Column(db.Integer, primary_key=True)
    x_username = db.Column(db.String(80), unique=True, nullable=False)
    x_bearer_token = db.Column(db.String(200), unique=True, nullable=True)
    x_consumer_key = db.Column(db.String(200), unique=True, nullable=True)
    x_consumer_secret = db.Column(db.String(200), unique=True, nullable=True)
    x_access_token = db.Column(db.String(200), unique=True, nullable=True)
    x_access_token_secret = db.Column(db.String(200), unique=True, nullable=True)

    def __repr__(self):
        return f'<User {self.username}>'