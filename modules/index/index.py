from flask import render_template, Blueprint

app = Blueprint('index', __name__, template_folder='../../templates')

@app.route('/')
def index():
    return render_template('index.html', logged=1)