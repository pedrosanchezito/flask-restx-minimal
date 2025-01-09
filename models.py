from app import db

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)

    def __repr__(self):
        return '<Item {}>'.format(self.name)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }