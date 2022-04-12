from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///energy.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.INTEGER, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    type = db.Column(db.SMALLINT, unique=False, nullable=False)

class User_Transaction(db.Model):
    id = db.Column(db.INTEGER, autoincrement=True, primary_key=True)
    user_id = db.Column(db.INTEGER, db.ForeignKey('user.id'), nullable=False)
    transaction_id = db.Column(db.INTEGER, db.ForeignKey('transaction.id'), nullable=False)
    type = db.Column(db.SMALLINT, nullable=False)
    user = db.relationship("User", backref="user_transaction")
    transaction = db.relationship("Transaction", backref="user_transaction")

class Transaction(db.Model):
    id = db.Column(db.INTEGER, autoincrement=True, primary_key=True)
    price = db.Column(db.DECIMAL, unique=False, nullable=False)
    energyAmount = db.Column(db.DECIMAL, unique=False, nullable=False)
    level = db.Column(db.SMALLINT, unique=False, nullable=False)
    flexibility = db.Column(db.BOOLEAN, unique=False, nullable=False)
    creationTimestamp = db.Column(db.String, unique=False, nullable=False)
    transactionTimestamp = db.Column(db.String, unique=False, nullable=False)
# Transaction(price=1.0, energyAmount=0.0, level=0, flexibility= False,creationTimestamp=datetime.datetime(), transactionTimestamp = datetime.datetime())
db.create_all()
# user = User(name="2",id="2",type=1)
# transaction
# db.session.add(user)
db.session.commit()

# db.session.add(Transaction(price=1.0, energyAmount=0.0, level=0, flexibility= False,creationTimestamp='21', transactionTimestamp = '1'))
