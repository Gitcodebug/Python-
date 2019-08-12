from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,PasswordField,SubmitField,BooleanField,DateTimeField
from wtforms.validators import DataRequired,Length,EqualTo,ValidationError,Email
from reading.models import User

class RegistrationForm(FlaskForm):
    username = StringField('用户名',validators=[DataRequired(),Length(min=2,max=16, message="用户名必须为2~16位")])
    email = StringField('邮箱',validators=[DataRequired(),Email()])
    password = PasswordField('密码',validators=[DataRequired()])
    confirm_password = PasswordField('确认密码',validators=[DataRequired(),EqualTo('password', message="请输入相同的密码")])
    submit = SubmitField('注册')
    def validate_username(self,username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('用户名已经被注册')
    def validate_email(self,email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('邮箱已被人注册')

class LoginForm(FlaskForm):
    email = StringField('邮箱',validators=[DataRequired(),Email()])
    password = PasswordField('密码',validators=[DataRequired()])
    # remember = BooleanField('Remember Me')
    submit = SubmitField('登录')

class RequestResetForm(FlaskForm):
    email = StringField('邮箱',validators=[DataRequired(),Email()])
    submit = SubmitField('提交')
    def validate_email(self,email):
        user = User.query.filter_by(email = email.data).first()
        if user is None:
            raise ValidationError('无效邮箱,请先注册')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('密码',validators=[DataRequired()])
    confirm_password = PasswordField('确认密码',validators=[DataRequired(),EqualTo('password', message="请输入相同的密码")])
    submit = SubmitField('重置密码')


    
class SearchForm(FlaskForm):
    searchword = StringField('搜索',validators=[DataRequired()])


class BooksForm(FlaskForm):
    bookname = StringField('书籍名',validators=[DataRequired()])
    booktype = StringField('书籍类型',validators=[DataRequired()])
    author = StringField('书籍作者',validators=[DataRequired()])
    image = StringField('书籍封面',validators=[DataRequired()])
    introduction = StringField('书籍介绍',validators=[DataRequired()])
    location = StringField('登记地址',validators=[DataRequired()])
    provider = IntegerField('图书拥有者',validators = [DataRequired()])
    submit = SubmitField("提交")

class OrderForm(FlaskForm):
    name = StringField('姓名',validators=[DataRequired()])
    bookname = StringField('书籍名',validators=[DataRequired()])
    address = StringField('接收地址',validators=[DataRequired()])
    telephone = StringField('联系电话',validators=[DataRequired()])
    submit= SubmitField("提交")

class MarketForm(FlaskForm):
    bookname = StringField('书籍名',validators=[DataRequired()])
    market = StringField('书评',validators=[DataRequired()])
    submit= SubmitField("提交")