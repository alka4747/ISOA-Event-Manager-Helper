from flask import Flask, render_template, request, abort

from competition import competition

app = Flask(__name__)

app.register_blueprint(competition, url_prefix='/api/competition')

# Accept only files smaller than 1MB
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form')
def form():
    user_requested_platform = request.args.get('platform')
    if user_requested_platform not in ['mulka', 'si-droid']:
        abort(400)
    return render_template('form.html', platform=user_requested_platform)