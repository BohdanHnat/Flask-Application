from app.database import db

class Event(db.Model):
    __tablename__ = 'event'

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_by_user = db.relationship('User')
    begin_at = db.Column(db.Date, nullable=False)
    end_at = db.Column(db.Date, nullable=False)
    max_users = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, default=False)

class EventUser(db.Model):
    __tablename__ = 'event_user'

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User')
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    event = db.relationship('Event')
    created_at = db.Column(db.Date, nullable=False)
    score = db.Column(db.Integer)