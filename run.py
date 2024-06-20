from app import app
from app.event import views
from app.main import views
from app.user import views
from flask import make_response

if __name__ == '__main__':
    app.run(port=app.config['PORT'], debug=app.config['DEBUG'])