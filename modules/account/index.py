from flask import render_template, Blueprint, session, redirect

app = Blueprint('account', __name__, template_folder='../../templates')

@app.route('/login')
def index():
    if 'user' in session:
        return redirect('/')
    return render_template('login.html')
@app.route('/logout')
def index2():
    del session['user']
    return redirect('/')