from flask import Blueprint, render_template, request
from models import db, Toy, Category, Combo, Comment

front_bp = Blueprint('front', __name__)


# 首页
@front_bp.route('/')
def index():
    featured_toys = Toy.query.order_by(db.func.random()).limit(8).all()
    popular_combos = Combo.query.order_by(Combo.price.desc()).limit(3).all()
    return render_template('front/index.html',
                           featured_toys=featured_toys,
                           popular_combos=popular_combos)


# 玩具详情
@front_bp.route('/toy/<int:toy_id>')
def toy_detail(toy_id):
    toy = Toy.query.get_or_404(toy_id)
    related_toys = Toy.query.filter_by(category_id=toy.category_id) \
        .filter(Toy.id != toy.id) \
        .limit(4).all()
    comments = Comment.query.filter_by(toy_id=toy_id).order_by(Comment.created_at.desc()).all()
    return render_template('front/toy_detail.html',
                           toy=toy,
                           related_toys=related_toys,
                           comments=comments)


# 添加评论
@front_bp.route('/toy/<int:toy_id>/comment', methods=['POST'])
def add_comment(toy_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    content = request.form['content']
    rating = int(request.form['rating'])

    comment = Comment(user_id=session['user_id'],
                      toy_id=toy_id,
                      content=content,
                      rating=rating)

    db.session.add(comment)
    db.session.commit()
    flash('评论已提交', 'success')
    return redirect(url_for('front.toy_detail', toy_id=toy_id))