from flask import Flask, redirect, url_for, session, render_template, request
import requests
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
        return redirect('/dashboard')
    return '<a href="/login">Login with Cognito</a>'


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

@app.route('/dashboard')
def dashboard():
    user = session.get('user')
    if not user:
        return redirect('/login')

    email = user.get('email', 'User')

    return render_template('dashboard.html', email=email)


@app.route('/slack/login')
def slack_login():
    slack_auth_url = (
        "https://slack.com/oauth/authorize"
        f"?client_id={os.getenv('SLACK_CLIENT_ID')}"
        f"&scope=identity.basic"
        f"&redirect_uri={os.getenv('SLACK_REDIRECT_URI')}"
    )
    return redirect(slack_auth_url)



@app.route('/slack/callback')
def slack_callback():
    code = request.args.get('code')
    if not code:
        return "Authorization failed or was canceled.", 400

    # Exchange code for access token
    response = requests.post("https://slack.com/api/oauth.access", data={
        'client_id': os.getenv('SLACK_CLIENT_ID'),
        'client_secret': os.getenv('SLACK_CLIENT_SECRET'),
        'code': code,
        'redirect_uri': os.getenv('SLACK_REDIRECT_URI')
    })


    token_data = response.json()
    if not token_data.get("ok"):
        return f"Slack auth failed: {token_data.get('error')}", 400

    # Get user info
    access_token = token_data['access_token']
    user_info_res = requests.get(
        "https://slack.com/api/users.identity",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    user_info = user_info_res.json()

    if not user_info.get("ok"):
        return f"Failed to fetch Slack user info: {user_info.get('error')}"

    user = user_info.get("user", {})
    return f"""
    <h1>Slack Login Successful</h1>
    <p>Welcome, {user.get('name')}</p>
    <p>Your Slack ID is {user.get('id')}</p>
    <p><a href="/dashboard">Back to Dashboard</a></p>
    """

if __name__ == '__main__':
    app.run(debug=True)