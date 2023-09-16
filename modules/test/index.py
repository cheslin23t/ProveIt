from flask import render_template, Blueprint

app = Blueprint('test', __name__, template_folder='../../templates')

@app.route('/test')
def index():
    return render_template('test.html')