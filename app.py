from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import datetime
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///energy.db'
app.config['SECRET_KEY'] = '1234'
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
# db.create_all()
# user = User(name="omar",id="1",type=1)
# transaction
# db.session.add(user)
# db.session.commit()

# db.session.add(Transaction(price=1.0, energyAmount=0.0, level=0, flexibility= False,creationTimestamp='21', transactionTimestamp = '1'))



@app.route('/', methods=["post", "get"])
def login():
    #return render_template("home.html")
    return render_template("login.html")

@app.route('/home', methods=["post", "get"])
def homepage():
    if request.method == 'GET':
        return render_template('home.html')

    elif request.method == 'POST':
        if request.form['submit_button'] == 'login':
            return render_template("login.html")
        elif request.form['submit_button'] == 'register':
            return render_template("create_user.html")



@app.route('/login', methods=["post"])
def loginin():
    # print(request.form["id"])
    user = User.query.get(request.form["id"])
    print(user.type)
    #buyer = 0
    if user.type == 0:
        messages = json.dumps(user.id)
        session['messages'] = messages
        return redirect('/transactions')
    elif user.type == 1:
        messages = json.dumps(user.id)
        session['messages'] = messages
        return redirect('/transaction/create')
    else:
        return redirect("/")

@app.route('/user/create')
def createUser():
    return render_template("create_user.html")

@app.route('/user/creation', methods=["post"])
def creationUser():
    user = User(name = request.form['name'], type = request.form['type'])
    db.session.add(user)
    db.session.commit()
    return redirect("/user/create")

@app.route('/transaction/create')
def createTranscation():
    id = json.loads(session['messages'])
    return render_template("create_transaction.html", items = id)

@app.route('/transaction/creation', methods=["post"])
def creationTransaction():
    transaction = Transaction( price = request.form['price'], energyAmount = request.form['energyAmount'], flexibility = True, level = request.form['level'], transactionTimestamp = request.form['transactionTimestamp'], creationTimestamp = str(datetime.datetime.now()) )
    user_transaction = User_Transaction( transaction= transaction, user= User.query.get(request.form['seller']),type=0)
    db.session.add(transaction)
    db.session.add(user_transaction)
    db.session.commit( )
    #return redirect("/transaction/create")
    return render_template("transactionsent.html")

@app.route('/transactions')
def transactions():
    trans = Transaction.query.all()
    id = json.loads(session['messages'])
    items = (id,trans)
    return render_template("transactions.html",items = items)

@app.route('/transaction/accept' ,methods=['POST'])
def transaction_accept():
    transaction = Transaction.query.get(request.form['transaction_id'])
    user_transaction = User_Transaction(transaction= transaction, user= User.query.get(request.form['user_id']),type=0)
    db.session.add(user_transaction)
    db.session.commit()
    return redirect("/transactions")