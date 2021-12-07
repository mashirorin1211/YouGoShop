from flask import request, render_template, url_for, redirect, flash, jsonify, abort
from flask_login import login_user, logout_user, login_required, current_user
import datetime
from main_project import app, db, bcrypt
from main_project.forms import RegisterForm, LoginForm, ItemForm, EditUserForm, TalkForm
from main_project.models import User, SellItem, WantItem, University, FirstCategory, SecondCategory, TalkItem, TrackItem, PurchaseItem, TrackingItem, ShopCartItem, TrackCartItem, TrackWantItem
import subprocess
import os, secrets
from PIL import Image

item_path = 'static/items'
user_path = 'static/users'

def category_verify(first, second):
    is_valid = SecondCategory.query.filter_by(id=second, first_id=first).first()
    is_valid if True else False
    
def get_form_selection(form):
    form.location.choices = [(location.id, location.name) for location in University.query.order_by(University.id.asc()).all()]
    form.category1.choices = [(first.id, first.name) for first in FirstCategory.query.order_by(FirstCategory.id.asc()).all()]
    form.category2.choices = [(second.id, second.name) for second in SecondCategory.query.all()]

#首頁
@app.route('/')
def index():
    db.create_all()
    return render_template('index.html', title='首頁')


#註冊、登入、登出
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(name = form.username.data, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        flash('註冊成功，您現在可以進行登入', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title="註冊", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('登入失敗，請確認輸入資訊是否正確!', 'danger')
    return render_template('login.html', title="登入", form=form)
               
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

#上傳
@app.route('/upload')
@login_required
def upload():
    return render_template('upload.html', title="上傳商品")

#追蹤
@app.route('/tracking/<string:user_name>')
def tracking(user_name):
    user = User.query.filter_by(name = user_name).first()
    if user is None:
        abort(404)
#    sells = sellItem.query.filter_by(who_id=user.id).order_by(sss.id.desc()).paginate(per_page=3, page=1)
    sells = TrackCartItem.query.filter_by(who_id=user.id).order_by(TrackCartItem.id.desc()).paginate(per_page=3, page=1)
#    wants = sellItem.query.filter_by(uploader_id=user.id).order_by(WantItem.id.desc()).paginate(per_page=3, page=1)
    wants = ShopCartItem.query.filter_by(who_id=user.id).order_by(ShopCartItem.id.desc()).paginate(per_page=3, page=1)
    want2s = TrackWantItem.query.filter_by(who_id=user.id).order_by(TrackWantItem.id.desc()).paginate(per_page=3, page=1)
    return render_template('tracking.html', title=f"{user.name}的頁面", user=user, sells=sells, wants=wants, want2s=want2s)

#儲存圖片
def save_image(form_image, target_path):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_image.filename)
    image_fn = random_hex + f_ext
    image_pt = os.path.join(app.root_path, target_path, image_fn)
    resize = (500, 500)
    i = Image.open(form_image)
    i.thumbnail(resize)
    i.save(image_pt)
    return image_fn
#取得分類
@app.route('/category/<int:first>')
def category(first):
    seconds = SecondCategory.query.filter_by(first_id=first).all()
    secondList = []
    for second in seconds:
        secondObj = {'id': second.id, 'name': second.name}
        secondList.append(secondObj)
    return jsonify({'seconds': secondList})


@app.route('/uploadSell', methods=['GET', 'POST'])
@login_required
def upload_sell():
    form = ItemForm()
    form.status.choices = [(1, '全新'), (2, '二手')]
    get_form_selection(form)
    if form.validate_on_submit() and form.image1.data:
        img1 = save_image(form.image1.data, item_path)
        img2 = save_image(form.image2.data, item_path) if form.image2.data else None
        img3 = save_image(form.image2.data, item_path) if form.image3.data else None
        new_item = SellItem(name=form.name.data, intro=form.intro.data,
            price=form.price.data, status_id=form.status.data, image1=img1, image2=img2, image3=img3,
            location_id=form.location.data,category1_id=form.category1.data, category2_id=form.category2.data,
            uploader_id=current_user.id
        )
        db.session.add(new_item)
        db.session.commit()
        flash('成功上傳販售商品', 'success')
        return redirect(url_for('index'))
    return render_template('uploadItem.html', title="上傳販售", form=form, heading_label="我要販售商品",
    price_label="商品售價", stat_label="商品狀態", cover_label="封面圖片", image2_label="商品圖一", image3_label="商品圖二")

@app.route('/uploadWant', methods=['GET', 'POST'])
@login_required
def upload_want():
    form = ItemForm()
    form.status.choices = [(1, '全新'), (2, '二手'), (3, '不限')]
    get_form_selection(form)
    if form.validate_on_submit() and form.image1.data:
        img1 = save_image(form.image1.data, item_path)
        img2 = save_image(form.image2.data, item_path) if form.image2.data else None
        img3 = save_image(form.image2.data, item_path) if form.image3.data else None
        new_item = WantItem(name=form.name.data, intro=form.intro.data,
            price=form.price.data, status_id=form.status.data, image1=img1, image2=img2, image3=img3,
            location_id=form.location.data,category1_id=form.category1.data, category2_id=form.category2.data,
            uploader_id=current_user.id
        )
        db.session.add(new_item)
        db.session.commit()
        flash('成功上傳徵求商品!', 'success')
        return redirect(url_for('index'))
    return render_template('uploadItem.html', form=form, title="上傳徵求", heading_label="我要徵求商品",
    price_label="預期價格", stat_label="預期狀態", cover_label="封面圖片", image2_label="相關圖一", image3_label="相關圖二")
    
@app.route('/user/<string:user_name>')
def user_overview(user_name):
    user = User.query.filter_by(name = user_name).first()
    if user is None:
        abort(404)
    sells = SellItem.query.filter_by(uploader_id=user.id).order_by(SellItem.id.desc()).paginate(per_page=3, page=1)
    wants = WantItem.query.filter_by(uploader_id=user.id).order_by(WantItem.id.desc()).paginate(per_page=3, page=1)
    return render_template('user.html', title=f"{user.name}的頁面", user=user, sells=sells, wants=wants)
@app.route('/user/<string:user_name>/info')
def user_info(user_name):
    user = User.query.filter_by(name = user_name).first()
    if user is None:
        abort(404)
    intro = user.intro.split('\n')
    return render_template('userInfo.html', title=f"{user.name}的檔案", user=user, intro=intro)

@app.route('/user/<string:user_name>/sellItems')
def user_sells(user_name):
    user = User.query.filter_by(name = user_name).first()
    page_num = request.args.get('page', 1, type=int)
    sellItems = SellItem.query.filter_by(uploader_id=user.id).order_by(SellItem.id.desc()).paginate(per_page=6, page=page_num)
    return render_template('onlineSells.html', title=f"{user.name}的販售商品", user=user, onlineItems=sellItems)

@app.route('/user/<string:user_name>/wantItems')
def user_wants(user_name):
    user = User.query.filter_by(name = user_name).first()
    page_num = request.args.get('page', 1, type=int)
    wantItems = WantItem.query.filter_by(uploader_id=user.id).order_by(WantItem.id.desc()).paginate(per_page=6, page=page_num)
    return render_template('onlineWants.html', title=f"{user.name}的徵求商品", user=user, onlineItems=wantItems)

@app.route('/user/edit', methods=['GET', 'POST'])
@login_required
def edit_user():
    user = User.query.get(current_user.id)
    form = EditUserForm(obj=user)
    form.gender.choices = [(1, '男性'), (2, '女性'), (3, '其他')]
    get_form_selection(form)
    if form.validate_on_submit():
        if form.image.data != user.image:
            if user.image != 'default.png':
                os.remove(url_for('static', filename=f'users/{user.image}'))
            new_image = save_image(form.image.data, user_path)
            user.image = new_image
        user.intro = form.intro.data
        user.gender = form.gender.data
        user.school_id = form.location.data
        user.favor1_id = form.category1.data
        user.favor2_id = form.category2.data
        db.session.commit()
        flash('成功修改個人資料', 'success')
        return redirect(url_for('index'))
    elif request.method == 'GET':
        form.location.data = user.school_id
        form.category1.data = user.favor1_id
        form.category2.data = user.favor2_id
    image_file = url_for('static', filename=f'users/{user.image}')
    return render_template('editUser.html', title="個人資料", user=user, form=form, image_file=image_file)


@app.route('/sellItem/<int:item_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_sell(item_id):
    item = SellItem.query.get_or_404(item_id)
    if item.uploader != current_user:
        abort(403)
    form = ItemForm(obj=item)
    form.status.choices = [(1, '全新'), (2, '二手')]
    get_form_selection(form)
    if form.validate_on_submit():
        if form.image1.data != item.image1:
            if item.image1:
                os.remove(os.path.join(app.root_path, item_path, item.image1))
            img1 = save_image(form.image1.data, item_path)
            item.image1 = img1
        if form.image2.data != item.image2:
            if item.image2:
                os.remove(os.path.join(app.root_path, item_path, item.image2))
            img2 = save_image(form.image2.data, item_path)
            item.image2 = img2
        if form.image3.data != item.image3:
            if item.image3:
                os.remove(os.path.join(app.root_path, item_path, item.image3))
            img3 = save_image(form.image3.data, item_path)
            item.image3 = img3
        item.name = form.name.data
        item.intro = form.intro.data
        item.price = form.price.data
        item.status_id = form.status.data
        item.location_id = form.location.data
        item.category1_id = form.category1.data
        item.category2_id = form.category2.data
        db.session.commit()
        flash('成功修改販售商品資訊', 'success')
        return redirect(url_for('sell_detail', sell_id=item.id))
    elif request.method == 'GET':
        form.status.data = item.status_id
        form.location.data = item.location_id
        form.category1.data = item.category1_id
        form.category2.data = item.category2_id
    imged1 = url_for('static', filename=f'items/{item.image1}')
    return render_template('editItem.html', title="編輯販售", form=form, item=item,
        heading_label="編輯販售商品", price_label="商品售價", stat_label="商品狀態", 
        cover_label="封面圖片", image2_label="商品圖一", image3_label="商品圖二",
        cover_image=imged1)

@app.route("/sellItem/<int:item_id>/delete", methods=['POST'])
@login_required
def delete_sell(item_id):
    item = SellItem.query.get_or_404(item_id)
    if item.uploader_id != current_user.id:
        abort(403)
    if item.image1:
        os.remove(os.path.join(app.root_path, item_path, item.image1))
    if item.image2:
        os.remove(os.path.join(app.root_path, item_path, item.image2))
    if item.image3:
        os.remove(os.path.join(app.root_path, item_path, item.image3))
    db.session.delete(item)
    db.session.commit()
    flash('成功刪除商品!', 'success')
    return redirect(url_for('user_sells', user_name=item.uploader.name))

@app.route("/sellItem/<int:item_id>/delete/<int:image_num>", methods=['POST'])
@login_required
def delete_sell_image(item_id, image_num):
    item = SellItem.query.get_or_404(item_id)
    if item.uploader_id != current_user.id:
        abort(403)
    if item.image2 and image_num == 2:
        os.remove(os.path.join(app.root_path, item_path, item.image2))
        item.image2 = None
    elif item.image3 and image_num == 3:
        os.remove(os.path.join(app.root_path, item_path, item.image3))
        item.image3 = None
    else:
        abort(404)
    db.session.commit()
    flash('成功刪除商品圖片!', 'success')
    return redirect(url_for('edit_sell', item_id=item_id))

@app.route('/wantItem/<int:item_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_want(item_id):
    item = WantItem.query.get_or_404(item_id)
    if item.uploader != current_user:
        abort(403)
    form = ItemForm(obj=item)
    form.status.choices = [(1, '全新'), (2, '二手'), (3, '不限')]
    get_form_selection(form)
    if form.validate_on_submit():
        if form.image1.data != item.image1:
            if item.image1:
                os.remove(os.path.join(app.root_path, item_path, item.image1))
            img1 = save_image(form.image1.data, item_path)
            item.image1 = img1
        if form.image2.data != item.image2:
            if item.image2:
                os.remove(os.path.join(app.root_path, item_path, item.image2))
            img2 = save_image(form.image2.data, item_path)
            item.image2 = img2
        if form.image3.data != item.image3:
            if item.image3:
                os.remove(os.path.join(app.root_path, item_path, item.image3))
            img3 = save_image(form.image3.data, item_path)
            item.image3 = img3
        item.name = form.name.data
        item.intro = form.intro.data
        item.price = form.price.data
        item.status_id = form.status.data
        item.location_id = form.location.data
        item.category1_id = form.category1.data
        item.category2_id = form.category2.data
        db.session.commit()
        flash('成功修改徵求商品資訊', 'success')
        return redirect(url_for('want_detail', want_id=item.id))
    elif request.method == 'GET':
        form.status.data = item.status_id
        form.location.data = item.location_id
        form.category1.data = item.category1_id
        form.category2.data = item.category2_id
    imged1 = url_for('static', filename=f'items/{item.image1}')
    return render_template('editItem.html', title="編輯徵求", form=form, item=item,
        heading_label="編輯徵求商品", price_label="預期價格", stat_label="預期狀態", 
        cover_label="封面圖片", image2_label="相關圖一", image3_label="相關圖二",
        cover_image=imged1)
        
@app.route("/wantItem/<int:item_id>/delete", methods=['POST'])
@login_required
def delete_want(item_id):
    item = WantItem.query.get_or_404(item_id)
    if item.uploader_id != current_user.id:
        abort(403)
    if item.image1:
        os.remove(os.path.join(app.root_path, item_path, item.image1))
    if item.image2:
        os.remove(os.path.join(app.root_path, item_path, item.image2))
    if item.image3:
        os.remove(os.path.join(app.root_path, item_path, item.image3))
    db.session.delete(item)
    db.session.commit()
    flash('成功刪除商品!', 'success')
    return redirect(url_for('user_wants', user_name=item.uploader.name))

@app.route("/wantItem/<int:item_id>/delete/<int:image_num>", methods=['POST'])
@login_required
def delete_want_image(item_id, image_num):
    item = WantItem.query.get_or_404(item_id)
    if item.uploader_id != current_user.id:
        abort(403)
    if item.image2 and image_num == 2:
        os.remove(os.path.join(app.root_path, item_path, item.image2))
        item.image2 = None
    elif item.image3 and image_num == 3:
        os.remove(os.path.join(app.root_path, item_path, item.image3))
        item.image3 = None
    else:
        abort(404)
    db.session.commit()
    flash('成功刪除商品圖片!', 'success')
    return redirect(url_for('edit_want', item_id=item_id))

@app.route('/online')
def online():
    return render_template('online.html', title="線上商品")
@app.route('/onlineSell')
def online_sell():
    page_num = request.args.get('page', 1, type=int)
    items = SellItem.query.order_by(SellItem.id.desc()).paginate(per_page=6, page=page_num)
    return render_template('onlineSells.html', title="線上販售商品", onlineItems=items, target="onlineSell")
@app.route('/onlineWant')
def online_want():
    page_num = request.args.get('page', 1, type=int)
    items = WantItem.query.order_by(WantItem.id.desc()).paginate(per_page=6, page=page_num)
    return render_template('onlineWants.html', title="線上徵求商品", onlineItems=items, target="onlineWant")

@app.route('/sellItem/<int:sell_id>')
def sell_detail(sell_id):
    user = User.query.get(current_user.id)
    item = SellItem.query.get_or_404(sell_id)
    intro = item.intro.split('\n')
    return render_template('sellDetail.html', user=user, item=item, intro=intro)
@app.route('/wantItem/<int:want_id>')
def want_detail(want_id):
    user = User.query.get(current_user.id)
    item = WantItem.query.get_or_404(want_id)
    intro = item.intro.split('\n')
    return render_template('wantDetail.html', user=user, item=item, intro=intro)

@app.route('/chat_user', methods=['GET', 'POST'])
@login_required
def chat_user():
    page_num = request.args.get('page', 1, type=int)
    items = TalkItem.query.order_by(TalkItem.id.desc()).paginate(per_page=100, page=page_num)
    form = TalkForm()
#    get_form_selection(form)
#    if form.validate_on_submit() and form.image1.data:
    if form.image1.data:
        datetime_dt = datetime.datetime.today()
        datetime_str = datetime_dt.strftime("%Y/%m/%d %H:%M:%S")
        img1 = save_image(form.image1.data, item_path)
        new_item = TalkItem(name=form.name.data, intro=form.intro.data,
            price=datetime_str, image1=img1,
            uploader_id=current_user.name
        )
        db.session.add(new_item)
        db.session.commit()
        flash('成功上傳意見', 'success')
        return redirect(url_for('index'))
    return render_template('chat_user.html', title="發送意見", form=form, heading_label="聊聊天視窗",
    price_label="發生時間" , cover_label="圖片附件" , onlineItems=items, target="onlineWant")

@app.route('/onlineTalk')
def online_Talk():
#    user = User.query.get(current_user.id)
#    item = SellItem.query.get_or_404(sell_id)
#    intro = item.intro.split('\n')
    page_num = request.args.get('page', 1, type=int)
    items = TalkItem.query.order_by(TalkItem.id.desc()).paginate(per_page=100, page=page_num)
    return render_template('onlineTalk.html', title="大家聊聊天", onlineItems=items, target="onlineWant")

@app.route("/talkItem/<int:item_id>/delete", methods=['GET'])
@login_required
def delete_talk(item_id):
    item = TalkItem.query.get_or_404(item_id)
#    if uploader_id!=current_user.name:
#        abort(403)
    db.session.delete(item)
    db.session.commit()
    flash('成功刪除留言', 'success')
    page_num = request.args.get('page', 1, type=int)
    items = TalkItem.query.order_by(TalkItem.id.desc()).paginate(per_page=100, page=page_num)
    return render_template('onlineTalk.html', title="大家聊聊天", onlineItems=items, target="onlineWant")

@app.route('/sellItem/<int:sell_id>/track')
def sell_detail_track(sell_id):
    user = User.query.get(current_user.id)
    item = SellItem.query.get_or_404(sell_id)
    intro = item.intro.split('\n')
    new_item = TrackItem(track_id=current_user.id,user_id=sell_id)
    db.session.add(new_item)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/sellItem/<int:item_id>/purchase', methods=['GET', 'POST'])
@login_required
def purchase_sell(item_id):
    item = SellItem.query.get_or_404(item_id)
#    if item.uploader == current_user:
#        abort(403)
    new_item = PurchaseItem(name = item.name , buy_name = current_user.name , intro = item.intro , price = item.price)
    db.session.add(new_item)
    db.session.commit()
    flash('成功購買販售商品', 'success')
    return redirect(url_for('sell_detail', sell_id=item.id))

@app.route('/sellItem/<int:item_id>/tracking', methods=['GET', 'POST'])
@login_required
def tracking_sell(item_id):
    item = SellItem.query.get_or_404(item_id)
#    if item.uploader == current_user:
#        abort(403)
#    new_item = TrackingItem(name = item.name , buy_name = current_user.name , intro = item.intro , price = item.price)
    new_item = TrackCartItem(name=item.name, intro=item.intro,
        price=item.price, status_id=item.status_id, image1=item.image1, image2=item.image2, image3=item.image3,
        location_id=item.location_id,category1_id=item.category1_id, category2_id=item.category2_id,
        who_id=current_user.id
    )
    db.session.add(new_item)
    db.session.commit()
    flash('成功追蹤商品', 'success')
    return redirect(url_for('sell_detail', sell_id=item.id))

@app.route('/sellItem/<int:item_id>/shopcart', methods=['GET', 'POST'])
@login_required
def shopcart_sell(item_id):
    item = SellItem.query.get_or_404(item_id)
#    if item.uploader == current_user:
#        abort(403)
    new_item = ShopCartItem(name=item.name, intro=item.intro,
        price=item.price, status_id=item.status_id, image1=item.image1, image2=item.image2, image3=item.image3,
        location_id=item.location_id,category1_id=item.category1_id, category2_id=item.category2_id,
        who_id=current_user.id
    )
    db.session.add(new_item)
    db.session.commit()
    flash('成功將商品加入購物車', 'success')
    return redirect(url_for('sell_detail', sell_id=item.id))


@app.route("/trackinga/<int:sell_id>/delete", methods=['GET'])
@login_required
def delete_track(sell_id):
    item = TrackCartItem.query.get_or_404(sell_id)
#    if uploader_id!=current_user.name:
#        abort(403)
    db.session.delete(item)
    db.session.commit()
    flash('成功刪除購物車', 'success')
    user = User.query.filter_by(name = current_user.name).first()
#    user = str(current_user.name)
    sells = TrackCartItem.query.filter_by(who_id=user.id).order_by(TrackCartItem.id.desc()).paginate(per_page=3, page=1)
    wants = ShopCartItem.query.filter_by(who_id=user.id).order_by(ShopCartItem.id.desc()).paginate(per_page=3, page=1)
    want2s = TrackWantItem.query.filter_by(who_id=user.id).order_by(TrackWantItem.id.desc()).paginate(per_page=3, page=1)
    return render_template('tracking.html', title=f"{user.name}的頁面", user=user, sells=sells, wants=wants, want2s=want2s)
#    flash('成功刪除購物車', 'success')
#    page_num = request.args.get('page', 1, type=int)
#    items = TalkItem.query.order_by(TalkItem.id.desc()).paginate(per_page=100, page=page_num)
#    return render_template('onlineTalk.html', title="大家聊聊天", onlineItems=items, target="onlineWant")

@app.route("/trackingb/<int:want_id>/delete", methods=['GET'])
@login_required
def delete_shopcart(want_id):
    item = ShopCartItem.query.get_or_404(want_id)
#    if uploader_id!=current_user.name:
#        abort(403)
    db.session.delete(item)
    db.session.commit()
    flash('成功刪除正在追蹤', 'success')
    user = User.query.filter_by(name = current_user.name).first()
#    user = str(current_user.name)
    sells = TrackCartItem.query.filter_by(who_id=user.id).order_by(TrackCartItem.id.desc()).paginate(per_page=3, page=1)
    wants = ShopCartItem.query.filter_by(who_id=user.id).order_by(ShopCartItem.id.desc()).paginate(per_page=3, page=1)
    want2s = TrackWantItem.query.filter_by(who_id=user.id).order_by(TrackWantItem.id.desc()).paginate(per_page=3, page=1)
    return render_template('tracking.html', title=f"{user.name}的頁面", user=user, sells=sells, wants=wants, want2s=want2s)

@app.route('/wantItem/<int:item_id>/wanttrack', methods=['GET', 'POST'])
@login_required
def tracking_want(item_id):
    item = WantItem.query.get_or_404(item_id)
#    if item.uploader == current_user:
#        abort(403)
#    new_item = TrackingItem(name = item.name , buy_name = current_user.name , intro = item.intro , price = item.price)
    new_item = TrackWantItem(name=item.name, intro=item.intro,
        price=item.price, status_id=item.status_id, image1=item.image1, image2=item.image2, image3=item.image3,
        location_id=item.location_id,category1_id=item.category1_id, category2_id=item.category2_id,
        who_id=current_user.id
    )
    db.session.add(new_item)
    db.session.commit()
    flash('成功追蹤商品', 'success')
    return redirect(url_for('want_detail', want_id=item.id))

@app.route("/trackingc/<int:want2_id>/delete", methods=['GET'])
@login_required
def delete_shopcart2(want2_id):
    item = TrackWantItem.query.get_or_404(want2_id)
#    if uploader_id!=current_user.name:
#        abort(403)
    db.session.delete(item)
    db.session.commit()
    flash('成功刪除正在追蹤', 'success')
    user = User.query.filter_by(name = current_user.name).first()
#    user = str(current_user.name)
    sells = TrackCartItem.query.filter_by(who_id=user.id).order_by(TrackCartItem.id.desc()).paginate(per_page=3, page=1)
    wants = ShopCartItem.query.filter_by(who_id=user.id).order_by(ShopCartItem.id.desc()).paginate(per_page=3, page=1)
    want2s = TrackWantItem.query.filter_by(who_id=user.id).order_by(TrackWantItem.id.desc()).paginate(per_page=3, page=1)
    return render_template('tracking.html', title=f"{user.name}的頁面", user=user, sells=sells, wants=wants, want2s=want2s)

if __name__ == '__main__':
#    os.system("sqlite_web -H 0.0.0.0 -x -p 8282 main_project/yougoshop.db&")
    app.run(host='0.0.0.0',port=5002,debug=True)

