from app import db

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(30), unique=False, nullable=False)
    name = db.Column(db.String(50), unique=False, nullable=False)
    address = db.Column(db.String(300), unique=False, nullable=False)
    rating = db.Column(db.String(5), unique=False, nullable=False)
    distance = db.Column(db.String(10), unique=False, nullable=False)
    duration = db.Column(db.Integer(), unique=False, nullable=False)
    # photo = db.Column(db.String(60), unique=False, nullable=False)

    def __repr__(self):
        return f"Result('{self.origin}, {self.name}', '{self.address}', '{self.rating}', '{self.distance}', '{self.duration}')"
