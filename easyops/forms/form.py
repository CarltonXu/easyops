from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class LoginForm(FlaskForm):
    username = StringField("用户名", validators=[DataRequired(message="用户名不能为空"), Length(min=5, max=20, message="用户名长度为5~20位")])
    password = PasswordField("密码", validators=[DataRequired(message="密码不能为空"), Length(min=5, max=120, message="密码长度为8~120位")])
    verify_code = StringField("验证码", validators=[DataRequired(message="验证码不能为空"), Length(min=4, max=4, message="验证码长度为4位")])
    submit = SubmitField("登录")

class RegisterForm(FlaskForm):
    username = StringField("用户名", validators=[DataRequired(message="用户名不能为空"), Length(min=5, max=20, message="用户名长度为5~20位")])
    password = PasswordField("密码", validators=[DataRequired(message="密码不能为空"), Length(min=8, max=120, message="密码长度为8~120位")])
    repassword = PasswordField("确认密码", validators=[DataRequired(message="确认密码不能为空"), Length(min=8, max=120, message="确认密码长度为8~120位"), EqualTo("password", message="密码必须一致")]) 
    submit = SubmitField("提交注册")

class ResetPasswordForm(FlaskForm):
    username = StringField("用户名", validators=[DataRequired(message="用户名不能为空"), Length(min=5, max=20, message="用户名长度为5~20位")])
    password = PasswordField("原密码", validators=[DataRequired(message="密码不能为空"), Length(min=8, max=120, message="密码长度为8~120位")])
    resetpassword = PasswordField("新密码", validators=[DataRequired(message="新密码不能为空"), Length(min=8, max=120, message="确认密码长度为8~120位")])
    submit = SubmitField("重置密码")