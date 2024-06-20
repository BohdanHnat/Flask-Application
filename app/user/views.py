from app import app
from app.database import db
from app.user.models import User
from app.user.forms import UserForm
from app.main.views import login_decorator
from flask import render_template, session, request, redirect, url_for
from flask.views import View

@app.get('/users')
@login_decorator
def users():
    users_data = User.query.all()
    return render_template('user/list.html', header='Users list',
                           username=session.get('username', 'Unknown user'), users_data=users_data,
                           selected_page=int(request.args.get('page', 0)), page_size=int(request.args.get('size', 1)))
@app.post('/register')
def register_user():
    form = UserForm()
    if form.validate():
        user = User()
        form.populate_obj(user)

        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login_page'))
    else:
        return form.errors
class ListView(View):
    def __init__(self, model, template):
        self.model = model
        self.template = template

    def dispatch_request(self):
        items_data = self.model.query.all()
        return render_template(self.template, items_data=items_data, username=session.get('username', 'Unknown'))
class DetailView(View):
    def __init__(self, model, template):
        self.model = model
        self.template = template

    def dispatch_request(self, id):
        item_data = self.model.query.get(id)
        return render_template(self.template, item_data=item_data, id=id, username=session.get('username', 'Unknown'))

app.add_url_rule(
    '/class/users',
    view_func=ListView.as_view('users-list', User, 'class/list.html')
)
app.add_url_rule(
    '/class/users/<int:id>',
    view_func=DetailView.as_view('user-detail', User, 'class/detail.html')
)
