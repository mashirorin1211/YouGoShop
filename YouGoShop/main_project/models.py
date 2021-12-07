#借用 Flask-Login 提供的類別UserMixin放在User這個物件上
from datetime import datetime
from main_project import db, login_manager
from flask_login import UserMixin

#隨時取得目前使用者id
@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    gender = db.Column(db.Integer)
    intro = db.Column(db.String(100), nullable=False, default='歡迎來到我的個人檔案')
    image = db.Column(db.String(25), nullable=False, default='default.png')
    school_id = db.Column(db.Integer, db.ForeignKey('university.id'), default=None)
    favor1_id = db.Column(db.Integer, db.ForeignKey('first_category.id'), default=None)
    favor2_id = db.Column(db.Integer, db.ForeignKey('second_category.id'), default=None)
    sell_item = db.relationship('SellItem', backref='uploader', lazy=True)
    want_item = db.relationship('WantItem', backref='uploader', lazy=True)
    sell_track = db.relationship('SellTrack', backref='tracker', lazy=True)
    want_track = db.relationship('WantTrack', backref='tracker', lazy=True)
    sell_record = db.relationship('SellRecord', backref='seller', lazy=True)
    want_record = db.relationship('WantRecord', backref='buyer', lazy=True)

class SellItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    intro = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('item_status.id'), nullable=False)
    image1 = db.Column(db.String(25), nullable=False)
    image2 = db.Column(db.String(25))
    image3 = db.Column(db.String(25))
    condition = db.Column(db.Integer, nullable=False, default=0)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    location_id = db.Column(db.Integer, db.ForeignKey('university.id'), nullable=False)
    category1_id = db.Column(db.Integer, db.ForeignKey('first_category.id'), nullable=False)
    category2_id = db.Column(db.Integer, db.ForeignKey('second_category.id'), nullable=False)
    uploader_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sell_track = db.relationship('SellTrack', backref='item', lazy=True)
    sell_record = db.relationship('SellRecord', backref='item', lazy=True)

class WantItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    intro = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('item_status.id'), nullable=False)
    image1 = db.Column(db.String(25), nullable=False)
    image2 = db.Column(db.String(25))
    image3 = db.Column(db.String(25))
    condition = db.Column(db.Integer, nullable=False, default=0)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    location_id = db.Column(db.Integer, db.ForeignKey('university.id'), nullable=False)
    category1_id = db.Column(db.Integer, db.ForeignKey('first_category.id'), nullable=False)
    category2_id = db.Column(db.Integer, db.ForeignKey('second_category.id'), nullable=False)
    uploader_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    want_track = db.relationship('WantTrack', backref='item', lazy=True)
    want_record = db.relationship('WantRecord', backref='item', lazy=True)

class University(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    user_id = db.relationship('User', backref='school', lazy=True)
    sellItem_id = db.relationship('SellItem', backref='location', lazy=True)
    wantItem_id = db.relationship('WantItem', backref='location', lazy=True)

class FirstCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    second_id = db.relationship('SecondCategory', backref='parent', lazy=True)
    user_favor1 = db.relationship('User', backref='favor1', lazy=True)
    sell_category1 = db.relationship('SellItem', backref='category1', lazy=True)
    want_category1 = db.relationship('WantItem', backref='category1', lazy=True)

class SecondCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    first_id = db.Column(db.Integer, db.ForeignKey('first_category.id'), nullable=False)
    user_favor2 = db.relationship('User', backref='favor2', lazy=True)
    sell_category1 = db.relationship('SellItem', backref='category2', lazy=True)
    want_category1 = db.relationship('WantItem', backref='category2', lazy=True)
    
class SellTrack(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sellItem_id = db.Column(db.Integer, db.ForeignKey('sell_item.id'), nullable=False)

class WantTrack(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    wantItem_id = db.Column(db.Integer, db.ForeignKey('want_item.id'), nullable=False)

class SellRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sellItem_id =db.Column(db.Integer, db.ForeignKey('sell_item.id'), nullable=False)

class WantRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sellItem_id = db.Column(db.Integer, db.ForeignKey('want_item.id'), nullable=False)

class ItemStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(5), nullable=False)
    sell_stat = db.relationship('SellItem', backref='status', lazy=True)
    want_stat = db.relationship('WantItem', backref='status', lazy=True)

class TalkItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    intro = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    image1 = db.Column(db.String(25), nullable=False)
    uploader_id = db.Column(db.String(50), nullable=False)

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    intro = db.Column(db.String(500), nullable=False)
    uploader_id = db.Column(db.String(50), nullable=False)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    intro = db.Column(db.String(500), nullable=False)
    uploader_id = db.Column(db.String(50), nullable=False)

class TrackItem(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    track_id = db.Column(db.Integer, primary_key=False)

class PurchaseItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    buy_name = db.Column(db.String(50), nullable=False)
    intro = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Integer, nullable=False)

class TrackingItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    buy_name = db.Column(db.String(50), nullable=False)
    intro = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Integer, nullable=False)

class ShopCartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    intro = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('item_status.id'), nullable=False)
    image1 = db.Column(db.String(25), nullable=False)
    image2 = db.Column(db.String(25))
    image3 = db.Column(db.String(25))
    condition = db.Column(db.Integer, nullable=False, default=0)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    location_id = db.Column(db.Integer, db.ForeignKey('university.id'), nullable=False)
    category1_id = db.Column(db.Integer, db.ForeignKey('first_category.id'), nullable=False)
    category2_id = db.Column(db.Integer, db.ForeignKey('second_category.id'), nullable=False)
    who_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class TrackCartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    intro = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('item_status.id'), nullable=False)
    image1 = db.Column(db.String(25), nullable=False)
    image2 = db.Column(db.String(25))
    image3 = db.Column(db.String(25))
    condition = db.Column(db.Integer, nullable=False, default=0)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    location_id = db.Column(db.Integer, db.ForeignKey('university.id'), nullable=False)
    category1_id = db.Column(db.Integer, db.ForeignKey('first_category.id'), nullable=False)
    category2_id = db.Column(db.Integer, db.ForeignKey('second_category.id'), nullable=False)
    who_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class TrackWantItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    intro = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('item_status.id'), nullable=False)
    image1 = db.Column(db.String(25), nullable=False)
    image2 = db.Column(db.String(25))
    image3 = db.Column(db.String(25))
    condition = db.Column(db.Integer, nullable=False, default=0)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    location_id = db.Column(db.Integer, db.ForeignKey('university.id'), nullable=False)
    category1_id = db.Column(db.Integer, db.ForeignKey('first_category.id'), nullable=False)
    category2_id = db.Column(db.Integer, db.ForeignKey('second_category.id'), nullable=False)
    who_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
