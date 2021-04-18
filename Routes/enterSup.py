from flask.blueprints import Blueprint
from flask import render_template
from flask import request
from flask import request, redirect, url_for

enterSup = Blueprint('enterSup', __name__,
                template_folder='templates',
                static_folder='static')


@enterSup.route('/enterSup', methods=['POST', 'GET'])
def enter_c():
    if request.method == 'POST':
        if (request.form.get('psw2')):
            psw1 =  request.form.get('psw2') 
            if psw1 == "admin":
                return redirect(url_for('support.index4'))

    return render_template('enterSup.html')
    