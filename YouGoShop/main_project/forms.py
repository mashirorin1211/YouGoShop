from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, RadioField, TextAreaField, SelectField
from wtforms.validators import DataRequired, InputRequired, Length, ValidationError, Optional
from flask_wtf.file import FileField, FileAllowed
from main_project.models import User

user_style = {'placeholder': '輸入長度限制為5~20字'}
password_style = {'placeholder': '輸入長度限制為8~20字'}
intro_style = {'placeholder': '輸入長度限制為50字，不可為空', 'style':'height: 100px;'}
image_style = {'style': 'display: none;', 'accept':".jpg, .jpeg, .png"}

title_style = {'placeholder': '輸入長度限制為5~20字'}
description_style = {'placeholder': '輸入長度限制為250字', 'style':'height: 200px;'}

class RegisterForm(FlaskForm):
    username = StringField("使用者名稱", validators=[InputRequired(message="請輸入使用者名稱"), 
        Length(min=5, max=20, message='使用者名稱長度不符規定')], render_kw=user_style)
    password = PasswordField("密碼", validators=[InputRequired(message="請輸入密碼"), 
        Length(min=8, max=20, message="密碼長度不符規定")], render_kw=password_style)
    submit = SubmitField('註冊')
    def validate_username(self, username):
        existed = User.query.filter_by(name = username.data).first()
        if existed:
            raise ValidationError("此使用者名稱已被使用")

class LoginForm(FlaskForm):
    username = StringField("使用者名稱", validators=[InputRequired(message="請輸入使用者名稱")])
    password = PasswordField("密碼", validators=[InputRequired(message="請輸入密碼")])
    submit = SubmitField('登入')

class ItemForm(FlaskForm):
    name = StringField("商品名稱", validators=[InputRequired(message='請輸入名稱'), 
        Length(min=5, max=20, message='輸入長度限制為5~20個字')], render_kw=title_style)
    intro = TextAreaField("商品敘述", validators=[InputRequired(message='請輸入敘述'),
        Length(max=270, message='超過字數上限(250字)')], render_kw=description_style)
    price = IntegerField(validators=[InputRequired(message='請輸入價格')])
    status = RadioField(coerce=int, validators=[DataRequired(message='請選擇狀態')])
    image1 = FileField(validators=[FileAllowed(['jpg', 'jpeg', 'png'], message="只接受jpg, jpeg, png格式")], render_kw=image_style)
    image2 = FileField(validators=[FileAllowed(['jpg', 'jpeg', 'png'], message="只接受jpg, jpeg, png格式")], render_kw=image_style)
    image3 = FileField(validators=[FileAllowed(['jpg', 'jpeg', 'png'], message="只接受jpg, jpeg, png格式")], render_kw=image_style)
    location = SelectField("所在學校", coerce=int, validators=[DataRequired(message='請選擇商品位置')])
    category1 = SelectField(coerce=int, validators=[DataRequired(message='請選擇第一層分類')])
    category2 = SelectField(coerce=int, validators=[DataRequired(message='請選擇第二層分類')])
    submit = SubmitField()
    def check_location(self, location):
        if location.data == 0:
            raise ValidationError('請選擇有效位置')
    def check_category(self, category1, category2):
        if category1.data == 0 or category2.data == 0:
            raise ValidationError('請選擇有效分類')

class EditUserForm(FlaskForm):
    username = StringField("使用者名稱")
    intro = TextAreaField("簡介", validators=[DataRequired(message='自我介紹不可空白'), Length(max=70, message='超過字數上限(50字)')],render_kw=intro_style)
    location = SelectField("就讀學校", coerce=int, validators=[Optional()], default=None)
    category1 = SelectField(coerce=int, validators=[Optional()], default=None)
    category2 = SelectField(coerce=int, validators=[Optional()], default=None)
    gender = RadioField("性別", coerce=int, validators=[Optional()], default=None)
    image = FileField("變更頭貼", validators=[FileAllowed(['jpg', 'jpeg', 'png'], message="只接受jpg, jpeg, png格式")], render_kw=image_style)
    submit = SubmitField('儲存')

class TalkForm(FlaskForm):
    name = StringField("主題", validators=[InputRequired(message='請輸入主題'),
        Length(min=5, max=20, message='輸入長度限制為5~20個字')], render_kw=title_style)
    intro = TextAreaField("內容", validators=[InputRequired(message='請輸入內容'),
        Length(max=270, message='超過字數上限(250字)')], render_kw=description_style)
    price = IntegerField(validators=[InputRequired(message='請輸入時間')])
    image1 = FileField(validators=[FileAllowed(['jpg', 'jpeg', 'png'], message="只接受jpg, jpeg, png格式")], render_kw=image_style)
    submit = SubmitField('送出')

class TrackForm(FlaskForm):
    user_id = TextAreaField("內容", validators=[InputRequired(message='請輸入內容'),
        Length(max=270, message='超過字數上限(250字)')], render_kw=description_style)
    track_id = TextAreaField("內容", validators=[InputRequired(message='請輸入內容'),
        Length(max=270, message='超過字數上限(250字)')], render_kw=description_style)

class PurchaseForm(FlaskForm):
    name = StringField("名稱", validators=[InputRequired(message='請輸入名稱'),
        Length(min=5, max=20, message='輸入長度限制為5~20個字')], render_kw=title_style)
    buy_name = StringField("名稱", validators=[InputRequired(message='請輸入名稱'),
        Length(min=5, max=20, message='輸入長度限制為5~20個字')], render_kw=title_style)
    intro = TextAreaField("商品敘述", validators=[InputRequired(message='請輸入敘述'),
        Length(max=270, message='超過字數上限(250字)')], render_kw=description_style)
    price = IntegerField(validators=[InputRequired(message='請輸入價格')])
