from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


saves = db.Table('saves',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('pin_id', db.Integer, db.ForeignKey('pin.id'), primary_key=True)
)



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    pins = db.relationship('Pin', backref='author', lazy=True)
    boards = db.relationship('Board', backref='creator', lazy=True)
    saved_pins = db.relationship('Pin', secondary=saves, lazy='subquery',
                                 backref=db.backref('savers', lazy=True))

    def __repr__(self):
        return f'<User {self.username}>'

# Pin model
class Pin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    image_url = db.Column(db.String(256), nullable=False)
    description = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'), nullable=False)
    myntra = db.Column(db.Boolean, default=False)  # New boolean column
    myntraid =  db.Column(db.Integer)
    def __repr__(self):
        return f'<Pin {self.title}>'

class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pins = db.relationship('Pin', backref='board', lazy=True)

    def __repr__(self):
        return f'<Board {self.name}>'


class MyntraUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # Adjust the backref to match the renamed relationship
    my_products = db.relationship('Product', secondary='user_product', lazy='subquery',
                                  backref=db.backref('users', lazy=True))

    def __repr__(self):
        return f'<MyntraUser {self.username}>'



class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(256))
    price = db.Column(db.Float)
    image_url = db.Column(db.String(256), nullable=False)
    ratings = db.Column(db.Float)
    # Rename 'my_users' to 'users' or another suitable name
    usersp = db.relationship('MyntraUser', secondary='user_product', lazy='subquery',
                            backref=db.backref('products', lazy=True))

    def __repr__(self):
        return f'<Product {self.name}>'



user_product = db.Table('user_product',
    db.Column('user_id', db.Integer, db.ForeignKey('myntra_user.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
)