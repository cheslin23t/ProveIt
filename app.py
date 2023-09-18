from flask import Flask, render_template, send_from_directory, session
from dotenv import load_dotenv
import os
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('flasksession')
activeRoutes=['index', 'account']
from importlib import import_module
from datetime import timedelta
for route in activeRoutes:
    print(route)
    m = import_module(f'modules.{route}.index')
    app.register_blueprint(m.app)

@app.route('/static/<path:path>')
def send_report(path):
    return send_from_directory('static', path)
app.run(host='0.0.0.0', port=8080)