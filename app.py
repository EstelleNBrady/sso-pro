from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
import os, secrets

app = Flask(__name__)
app.config['SERVER_NAME'] = 'localhost:5000'  # Ensures url_for uses 'localhost' not '127.0.0.1'
app.secret_key = os.urandom(24)  # Encryption key for user sessions
oauth = OAuth(app)

# Register Cognito as an OAuth provider
oauth.register(
    name='cognito',
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    authorize_url='https://estelle-sso.auth.us-east-2.amazoncognito.com/oauth2/authorize',
    access_token_url='https://estelle-sso.auth.us-east-2.amazoncognito.com/oauth2/token',
    server_metadata_url='https://cognito-idp.us-east-2.amazonaws.com/us-east-2_PoG5vpGPd/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email'}
)

@app.route('/')
def index():
    user = session.get('user')
    if user:
        return f'Hello, {user.get("email", "User")}! <a href="/logout">Logout</a>'
    return '<a href="/login">Login</a>'


@app.route('/login')
def login():
    nonce = secrets.token_urlsafe(16)
    session['nonce'] = nonce
    redirect_uri = url_for('authorize', _external=True)
    return oauth.cognito.authorize_redirect(redirect_uri, nonce=nonce)


@app.route('/authorize')
def authorize():
    token = oauth.cognito.authorize_access_token()
    nonce = session.pop('nonce', None)
    user = oauth.cognito.parse_id_token(token, nonce=nonce)
    session['user'] = user
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)