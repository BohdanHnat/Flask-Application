from app import app
from app.user.models import User
from flask import render_template, request, session, redirect, url_for, make_response
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from werkzeug.security import check_password_hash, generate_password_hash
def authorized_decorator(func):
    @jwt_required()
    def wrapper(*args, **kwargs):
        identity = get_jwt_identity()
        username = identity['username']
        if username not in ['admin', 'user', 'root']:
            return make_response('', 401)
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper
def login_decorator(func):
    def wrapper(*args, **kwargs):
        if not session.get('username', None):
            return redirect(url_for('login_page'))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper
@app.route('/login', methods=['POST', 'GET'])
def login_page():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if (user and username == user.username) and password == user.password:
            session['username'] = username
            return redirect(url_for('get_events'))
        return render_template('main/login.html', username=session.get('username', 'Unknown'),
                               error='Invalid username or password')
    return render_template('main/login.html', username=session.get('username', 'Unknown'))

@app.get('/logout')
def logout_user():
    session.pop('username', None)
    return redirect(url_for('login_page'))

@app.post('/api/login')
def api_login():
    username = request.json.get('username')
    password = request.json.get('password')
    access_token = create_access_token(identity={'username': username})
    return {'token': access_token}
