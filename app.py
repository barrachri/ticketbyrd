from flask import Flask
from ticketbyrd.tickets import tickets_blueprint

from factory import db

app = Flask(__name__)
app.register_blueprint(tickets_blueprint)


if __name__ == '__main__':
    # run our standalone gevent server
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    app.run(port=8080)