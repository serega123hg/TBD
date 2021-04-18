from flask.blueprints import Blueprint
from flask import render_template
from flask import request
from flask import request, redirect, url_for

enterCall = Blueprint('enterCall', __name__,
                template_folder='templates',
                static_folder='static')


@enterCall.route('/enterCall', methods=['POST', 'GET'])
def enter_c():
    if request.method == 'POST':
        if (request.form.get('psw1')):
            psw1 =  request.form.get('psw1') 
            if psw1 == "admin":
                return redirect(url_for('callcenter.index5'))

    return render_template('enterCall.html')
    