from flask import Flask, render_template, send_from_directory
app = Flask(__name__)
activeRoutes=['index', 'test']
from importlib import import_module

for route in activeRoutes:
    print(route)
    m = import_module(f'modules.{route}.index')
    app.register_blueprint(m.app)

@app.route('/statoc/<path:path>')
def send_report(path):
    return send_from_directory('static', path)
app.run(host='0.0.0.0', port=8080)