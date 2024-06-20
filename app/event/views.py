from app import app
from app.database import db
from app.user.models import User
from app.user.views import ListView, DetailView
from app.event.models import Event, EventUser
from app.event.forms import EventForm, EventUserForm
from app.main.views import login_decorator, authorized_decorator
from flask import make_response, render_template, request, session, redirect
from datetime import date

@app.get('/events')
@login_decorator
def get_events():
    events_data = Event.query.all()
    event_users = EventUser.query

    current_user = User.query.filter_by(username=session.get('username')).one()
    user_registered_events_id = [event_user.event_id for event_user in EventUser.query.filter_by(user_id=current_user.id)]

    searched_title = [event.title for event in events_data if event.title == request.args.get('title', '')]

    return render_template('event/list.html', header='Events list',
                           username=session.get('username', 'Unknown'), events_data=events_data,
                           current_date=date.today(), registered_events_id=user_registered_events_id,
                           current_user_id=current_user.id, event_users_data=event_users, searched_title=searched_title,
                           selected_page=int(request.args.get('page', 0)), page_size=
                           int(request.args.get('size', 1)) if not searched_title else len(events_data))
@app.get('/events/<int:id>')
@login_decorator
def event_id(id):
    event_data = Event.query.get(id)
    return render_template('event/detail.html', id=id,
                           username=session.get('username', 'Unknown'), event_data=event_data)
app.add_url_rule(
    '/class/events',
    view_func=ListView.as_view('events-list', Event, 'class/list.html')
)
app.add_url_rule(
    '/class/events/<int:id>',
    view_func=DetailView.as_view('event-detail', Event, 'class/detail.html')
)
@app.route('/events/<int:id>/users', methods=['GET', 'POST'])
@login_decorator
def event_users(id):
    if request.method == 'POST':
        form = EventUserForm()
        if form.validate():
            event_user = EventUser()
            form.populate_obj(event_user)

            db.session.add(event_user)
            db.session.commit()
            return redirect(f'/events/{id}/users')
        else:
            return form.errors
    else:
        event_users = EventUser.query.filter_by(event_id=id).all()
        return render_template('event/event_users.html', id=id,
                           username=session.get('username', 'Unknown'), event_users=event_users)

@app.route('/events/<int:id>/update', methods=['GET', 'POST'])
@login_decorator
def update_event(id):
    if request.method == 'POST':
        form = EventForm()
        if form.validate():
            event = Event.query.get(id)
            for key, value in form.data.items():
                setattr(event, key, value)

            db.session.commit()
            return redirect(f'/events/{event.id}')
        else:
            return form.errors
    else:
        event_data = Event.query.get(id)
        return render_template('event/detail.html', id=id,
                               username=session.get('username', 'Unknown'), event_data=event_data)

@app.route('/events/create', methods=['GET', 'POST'])
@login_decorator
def create_event():
    if request.method == 'POST':
        form = EventForm()
        if form.validate():
            event = Event()
            form.populate_obj(event)

            db.session.add(event)
            db.session.commit()
            return redirect(f'/events/{event.id}')
        else:
            return form.errors
    else:
        return render_template('event/create.html', username=session.get('username', 'Unknown'))

@app.route('/api/events/', methods=['GET', 'POST'])
@authorized_decorator
def get_or_create_events_api():
    if request.method == 'GET':
        events_data = Event.query.all()
        events_data_dict = [{'id': event.id, 'title': event.title, 'description': event.description,
                            'created_by': event.created_by, 'begin_at': event.begin_at, 'end_at': event.end_at,
                             'max_users': event.max_users, 'is_active': event.is_active} for event in events_data]
        return events_data_dict
    else:
        return request.json, 201

@app.route('/api/users/', methods=['GET', 'POST'])
@authorized_decorator
def get_or_create_users_api():
    if request.method == 'GET':
        users_data = User.query.all()
        users_data_dict = [{'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name,
                            'username': user.username, 'password': user.password} for user in users_data]
        return users_data_dict
    else:
        return request.json, 201

@app.route('/api/events/<int:id>/', methods=['PATCH', 'DELETE'])
@authorized_decorator
def adjust_or_delete_event(id):
    if request.method == 'DELETE':
        response = make_response()
        response.status_code = 204
        return response
    else:
        return request.json, 200

@app.route('/api/events/<int:id>/users')
@authorized_decorator
def get_event_users_api(id):
    event_users_data = EventUser.query.all()
    event_users_data_dict = [{'id': event_user.id, 'user_id': event_user.user_id,
                              'event_id': event_user.event_id, 'created_at': event_user.created_at,
                              'score': event_user.score} for event_user in event_users_data]
    return event_users_data_dict

@app.route('/api/users/<int:id>/', methods=['PATCH', 'DELETE'])
@authorized_decorator
def adjust_or_delete_user(id):
    if request.method == 'DELETE':
        response = make_response()
        response.status_code = 204
        return response
    else:
        return request.json, 200



