from backend import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), index=True)
    fullname = db.Column(db.String(100), index=True)
    phoneno = db.Column(db.String(100), index=True)
    country = db.Column(db.String(100), index=True)
    password = db.Column(db.String(100), index=True)
    email = db.Column(db.String(120), index=True, unique=True)

    def __repr__(self):
        return flask.jsonify(username=self.username, fullname=self.fullname, email=self.email, phoneno=self.phoneno, country=self.country)