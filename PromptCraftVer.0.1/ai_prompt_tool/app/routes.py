## app/routes.py
from flask import render_template, url_for, flash, redirect, request, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from app import app, db
from app.forms import RegistrationForm, LoginForm
from app.models import User, Document

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/document", methods=['POST'])
@login_required
def create_document():
    title = request.json.get('title')
    content = request.json.get('content')
    if not title or not content:
        return jsonify({'error': 'Missing title or content'}), 400
    document = Document(title=title, content=content, owner=current_user)
    db.session.add(document)
    db.session.commit()
    return jsonify({'message': 'Document created successfully'}), 200

@app.route("/document", methods=['GET'])
@login_required
def get_document():
    title = request.args.get('title')
    document = Document.query.filter_by(title=title, user_id=current_user.id).first()
    if document:
        return jsonify({'title': document.title, 'content': document.content}), 200
    else:
        return jsonify({'error': 'Document not found'}), 404

@app.route("/document", methods=['PUT'])
@login_required
def update_document():
    title = request.json.get('title')
    new_content = request.json.get('new_content')
    document = Document.query.filter_by(title=title, user_id=current_user.id).first()
    if document:
        document.content = new_content
        db.session.commit()
        return jsonify({'message': 'Document updated successfully'}), 200
    else:
        return jsonify({'error': 'Document not found'}), 404

@app.route("/document", methods=['DELETE'])
@login_required
def delete_document():
    title = request.args.get('title')
    document = Document.query.filter_by(title=title, user_id=current_user.id).first()
    if document:
        db.session.delete(document)
        db.session.commit()
        return jsonify({'message': 'Document deleted successfully'}), 200
    else:
        return jsonify({'error': 'Document not found'}), 404
