from flask import Flask, flash, redirect, render_template, request, url_for
from flask import sessions
from flask.helpers import flash
from flask_login import LoginManager, UserMixin, login_user,logout_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.wrappers import UserAgentMixin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///studentregister.db"
app.config['SQLALCHEMY_BINDS']={'book':"sqlite:///book.db",'issue':"sqlite:///issue.db",'yourbook':"sqlite:///yourbook.db"}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '_5#y3L"F4Q8z\n\xec]/'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

class Form(UserMixin,db.Model):  
	id = db.Column(db.Integer, primary_key=True)
	sname = db.Column(db.String(10), nullable=False)
	email = db.Column(db.String(30),unique = True, nullable=False)
	phone = db.Column(db.String(12),unique = True, nullable=False)
	ssem = db.Column(db.String(12),nullable=False)
	cllgname = db.Column(db.String(30), nullable=True)
	pincode = db.Column(db.String(7), nullable=False)
	coursename = db.Column(db.String(15), nullable=False)
	username = db.Column(db.String(10),nullable=False)
	password = db.Column(db.String(10),nullable=False)
	def __repr__(self):
		return '<Form %r' % self.username

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/<string:user_page>", methods=['GET','POST'])
def page(user_page):
	if(request.method == 'POST'):
		sname = request.form['sname']
		email = request.form['email']
		phone = request.form['phone']
		ssem = request.form['ssem']
		cllgname = request.form['cllgname']
		pincode = request.form['pincode']
		coursename = request.form['coursename']
		username = request.form['username']
		password = request.form['password']

		entry = Form(sname=sname,email=email, phone=phone, cllgname=cllgname,pincode=pincode, coursename=coursename,username=username,password=password,ssem=ssem)
		
		db.session.add(entry)
		db.session.commit()
		flash('Registration Completed!','success')
		return render_template(user_page)
	
	return render_template(user_page)

@app.route("/studentinfo.html")
def sstudentinfo():
	students = Form.query.all()
	totals = Form.query.count()
	return render_template('studentinfo.html',students=students,totals=totals)

class Book(db.Model):
	__bind_key__ = 'book'
	book_id = db.Column(db.Integer, primary_key=True)
	bookname = db.Column(db.String(10), nullable=False)
	author = db.Column(db.String(10), nullable=False)
	numberofbooks = db.Column(db.String(10), nullable=False)
	semester = db.Column(db.String(10), nullable=False)
	
	def __repr__(self):
		return '<Books %r' % self.title	

@app.route("/addbook" ,methods=['GET','POST'])
def books():
	if(request.method == 'POST'):
		bookname = request.form['title']
		author = request.form['author']
		numberofbooks = request.form['book_count']
		semester = request.form['bsem']
		mybook = Book(bookname=bookname,author=author,numberofbooks=numberofbooks,semester=semester)
		db.session.add(mybook)
		db.session.commit()
		flash('Book added Successfully!','success')
		return render_template("updatebooks.html")
	
	return render_template("updatebooks.html")

class Issue(db.Model):
	__bind_key__ = 'issue'
	book_id = db.Column(db.Integer, primary_key=True)
	unique_id = db.Column(db.String(20), nullable=False)
	namebook = db.Column(db.String(20), nullable=False)
	booksem = db.Column(db.String(5), nullable=False)
	def __repr__(self):
		return '<Books %r' % self.title	

@app.route("/issuebook" ,methods=['GET','POST'])
def issuebook():
	if(request.method == 'POST'):
		unique_id = request.form['unique_id']
		namebook = request.form['namebook']
		booksem = request.form['booksem']
		mybook1 = Issue(unique_id=unique_id,namebook=namebook,booksem=booksem)
		db.session.add(mybook1)
		db.session.commit()
		ibook = Issue.query.count()
		flash('Book request sent Successfully!','success')
		return render_template("yourbooks.html",book_count=ibook)
	return render_template("yourbooks.html")

@app.route("/notifications.html")
def issuebook2():
	ibook = Issue.query.all()
	return render_template('notifications.html',ibook=ibook)

class Yourbook(db.Model):
	__bind_key__ = 'yourbook'
	book_id = db.Column(db.Integer, primary_key=True)

	yname = db.Column(db.String(30), nullable=False)
	title = db.Column(db.String(20), nullable=False)
	bsem = db.Column(db.String(5), nullable=False)

	def __repr__(self):
		return '<Books %r' % self.title	

@app.route("/yourbook" ,methods=['GET','POST'])
def yourbooks():
	if(request.method == 'POST'):

		yname = request.form['firstname']		
		title = request.form['title']
		bsem = request.form['bsem']

		sbook = Yourbook(yname=yname,title=title,bsem=bsem)
		db.session.add(sbook)
		db.session.commit()
		flash('Book has been Issued Successfully!','success')
		return render_template("notifications.html")
	return render_template("notifications.html")

@app.route("/yourbooks.html")
def yourbooks2():
	ybook = Yourbook.query.all()
	return render_template('yourbooks.html',ybook=ybook)

count = 0

@app.route("/libraryinfoT.html")
def showBooksONteacher():
	allbookT = Book.query.all()
	totalb = Book.query.count()
	totali = Issue.query.count()
	return render_template('libraryinfoT.html',allbookT=allbookT,count=count,totalb=totalb,totali=totali,totalr=int(totalb-totali))

@app.route("/libraryinfoS.html")
def showBooksONstud():
	allbookS = Book.query.all()
	return render_template('libraryinfoS.html',allbookS=allbookS)	

@login_manager.user_loader
def load_user(user_id):
	return Form.query.get(int(user_id))

# update
# @app.route("/update/<int:id>" ,methods=['GET','POST'])
# def update_book(id):
# 	upbook = Book.query.get()
# 	return redirect('/update.html')

# delete
@app.route("/delete/<int:id>")
def delete_book(id):
	Book_to_delete = Book.query.get_or_404(id)
	try:
		db.session.delete(Book_to_delete)
		db.session.commit()
	except:
		print("Sorry we can't delete data!")

	return redirect("/libraryinfoT.html")


@app.route("/login" ,methods=['GET','POST'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']

		user = Form.query.filter_by(username=username).first()

		if user and user.password == password:
			login_user(user)
			return redirect("/myprofile.html")
		else:
			flash("Invalid credentails!","danger")

	return redirect("studlogin.html")		

@app.route("/Tlogin" ,methods=['GET','POST'])
def Tlogin():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']

		Tuser = Form.query.filter_by(username=username).first()

		if Tuser and Tuser.password == password:
			login_user(Tuser)
			return redirect("/studentinfo.html")
		else:
			flash("Invalid credentails!","danger")

	return redirect("teacherlogin.html")

@app.route("/logout" ,methods=['GET','POST'])
def logout():
	logout_user()
	return redirect('/index.html')

if __name__ == "__main__":
	app.run(debug=True)

