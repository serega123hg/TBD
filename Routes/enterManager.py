from flask.blueprints import Blueprint
from flask import render_template
from flask import request, redirect, url_for

enterManager = Blueprint('enterManager', __name__,
                template_folder='templates',
                static_folder='static')


@enterManager.route('/enterManager', methods=['POST', 'GET'])
def enter_m():
    if request.method == 'POST':
        if (request.form.get('psw')):
            psw1 =  request.form.get('psw') 
            if psw1 == "admin":
                return redirect(url_for('manage.index3'))

    return render_template('enterManager.html')
    