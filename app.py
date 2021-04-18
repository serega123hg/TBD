import flask
from flask import Flask, render_template
from flask import request


from Routes.index import index1
from Routes.manage import manage
from Routes.support import support
from Routes.client import client
from Routes.driver import driver
from Routes.callcenter import callcenter

app = Flask(__name__)
app.config['DEBUG'] = True
app.register_blueprint(index1)
app.register_blueprint(manage)
app.register_blueprint(support)
app.register_blueprint(client)
app.register_blueprint(driver)
app.register_blueprint(callcenter)

if __name__ == "__main__":
    app.run()