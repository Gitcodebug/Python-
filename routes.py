from flask import render_template,url_for,flash,redirect,request
from reading.form import RegistrationForm,LoginForm,RequestResetForm,ResetPasswordForm,SearchForm,BooksForm,OrderForm,MarketForm
from reading.models import User,Books,BookMarket,Borrower
from reading import app, bcrypt, db, mail
from flask_login import login_user,logout_user,current_user
from flask_mail import Message

@app.route('/', methods = ['GET'])
def home():
    return render_template('home.html')

@app.route('/login', methods = ['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            # login_user(user,remember=form.remember.data)
            # return redirect(url_for('home')) 
            login_user(user)
            flash('登录成功')
            return redirect(url_for('home'))
        flash('登录失败')
    return render_template('login.html',form = form)

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('重置请求' , sender = 'noreply_reading@yeah.net' , recipients =[user.email])
    msg.body =f'''重置密码，请点击下面的链接：{url_for('reset_token',token = token,_external = True)}'''
    mail.send(msg)

def send_information_email(user,name,address,telephone,bookname):
    msg = Message('信息确认',sender = 'noreply_reading@yeah.net' ,recipients = [user.email])
    msg.body=f'''姓名:{name}
    收货地址:{address}
    联系方式:{telephone}
    书籍:{bookname}


请注意查收
如果不是本人操作，请忽略
不要回复本邮件'''
    mail.send(msg)



@app.route('/registe',methods=["GET","POST"])
def registe():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username = form.username.data,email = form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account Created for {form.username.data}','success')
        return redirect(url_for('login'))
    return render_template('registe.html',form = form)

    
@app.route('/logout',methods=["GET","POST"])
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/reset_request',methods=["GET","POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        send_reset_email(user)
        flash("邮件已发送，请重置密码")
        return redirect(url_for('login'))
    return render_template('reset_request.html',form = form) 

@app.route('/reset_password/<token>',methods=["GET","POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Error')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user.password = hashed_password
        db.session.commit()
        # flash(f'Account Created for {form.username.data}','success')
        return redirect(url_for('login'))
    return render_template('reset_token.html',form = form)



@app.route('/store')
def store():
    page = request.args.get('page',1,type=int)
    books = Books.query.paginate(page = page, per_page=16)
    return render_template('store.html',books = books, User=User)

@app.route('/search')
def search():
    form = SearchForm()
    searchmap =Books.query.filter_by(booktype=request.args['keywords'] )
    page = request.args.get('page',1,type=int)
    books = Books.query.paginate(page = page, per_page=16)
    return render_template('search.html',form=form,books=searchmap)

@app.route('/lentform',methods = ['GET','POST'])
def lentform():
    form = BooksForm()
    if form.validate_on_submit():
        books = Books(bookname = form.bookname.data,booktype = form.booktype.data, introduction = form.introduction.data, 
                        provider = form.provider.data,author = form.author.data,location = form.location.data, image = form.image.data)
        db.session.add(books)
        db.session.commit()
    return render_template('lentform.html',form = form)

@app.route('/personal')
def personal():
    return render_template('personal.html')

@app.route('/lend')
def lend():
    books = Books.query.filter_by(provider = current_user.id).all()
    return render_template('lend.html',books = books)

@app.route('/perinfor')
def perinfor():
    return render_template('perinfor.html')

@app.route('/orderform/<int:id>' ,methods=['GET', 'POST'])
def orderform(id):
    form = OrderForm()
    if form.validate_on_submit():
        # user = User.query.filter_by(email = form.email.data).first()
        user = User.query.get(id)
        name = form.name.data
        address = form.address.data
        telephone = form.telephone.data
        bookname = form.bookname.data
        print('===========')
        print(address)
        print('===========')
        send_information_email(user,name, address,telephone,bookname)
        flash("邮件已发送，请等待发货"+user.email)
        borrow = Borrower(bookname = form.bookname.data,userid = current_user.id,username = current_user.username)
        db.session.add(borrow)
        db.session.commit()
    return render_template('orderform.html',form = form )

@app.route('/bookmarket',methods=['GET','POST'])
def marketform():
    form = MarketForm()
    if form.validate_on_submit():
        print("ttttttttttttttttttttttttt")
        bookmarket = BookMarket(userid = current_user.id,bookname =form.bookname.data,market = form.market.data,username = current_user.username)
        db.session.add(bookmarket)
        db.session.commit()       
    return render_template('bookmarket.html',form = form)

@app.route('/markets',methods=['GET','POST'])
def markets():
    markets = BookMarket.query.all()
    return render_template('markets.html',markets=markets)

@app.route('/borrowed',methods=['GET','POST'])
def borrowed():
    borrower = Borrower.query.all()
    return render_template('borrowed.html',borrower = borrower)

