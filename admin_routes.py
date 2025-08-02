from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Combo, Toy, Category, Tag, User, Comment, Log
from utils.auth import admin_required

admin_bp = Blueprint('admin', __name__)


# 套餐管理
@admin_bp.route('/combos')
@login_required
@admin_required
def combo_list():
    combos = Combo.query.all()
    return render_template('admin/combos.html', combos=combos)


@admin_bp.route('/combo/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_combo():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        discount = float(request.form['discount'])
        price = float(request.form['price'])
        toy_ids = request.form.getlist('toys')

        combo = Combo(name=name, description=description,
                      discount=discount, price=price)

        for toy_id in toy_ids:
            toy = Toy.query.get(toy_id)
            if toy:
                combo.toys.append(toy)

        db.session.add(combo)
        db.session.commit()
        flash('套餐创建成功', 'success')
        return redirect(url_for('admin.combo_list'))

    toys = Toy.query.all()
    return render_template('admin/combo_form.html', toys=toys)


# 分类管理
@admin_bp.route('/categories')
@login_required
@admin_required
def category_list():
    categories = Category.query.filter_by(parent_id=None).all()
    return render_template('admin/categories.html', categories=categories)


# 用户管理
@admin_bp.route('/users')
@login_required
@admin_required
def user_list():
    users = User.query.all()
    return render_template('admin/users.html', users=users)


# 日志管理
@admin_bp.route('/logs')
@login_required
@admin_required
def log_list():
    page = request.args.get('page', 1, type=int)
    logs = Log.query.order_by(Log.created_at.desc()).paginate(page=page, per_page=20)
    return render_template('admin/logs.html', logs=logs)