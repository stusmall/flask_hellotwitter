from flask import Flask, session, flash, redirect, url_for, request
from flask_oauthlib.client import OAuth

app = Flask(__name__)

oauth = OAuth()
twitter = oauth.remote_app('twitter',
                           base_url='https://api.twitter.com/1/',
                           request_token_url='https://api.twitter.com/oauth/request_token',
                           access_token_url='https://api.twitter.com/oauth/access_token',
                           authorize_url='https://api.twitter.com/oauth/authenticate',
                           consumer_key='',#TODO: Fill in!
                           consumer_secret=''#TODO: Fill in!
                           )


@twitter.tokengetter
def get_twitter_token(token=None):
    return session.get('twitter_token')


@app.route('/')
def index():
    return 'Logged in as twitter user {}'.format(session['twitter_user'])


@app.route('/login')
def login():
    try:
        return twitter.authorize(callback=url_for('oauth_authorized',
                                              next=request.args.get('next') or request.referrer or None))
    except Exception as e:
        print("Some type of exception {}".format(e))

@app.route('/oauth-authorized')
def oauth_authorized():
    next_url = request.args.get('next') or url_for('index')
    resp = twitter.authorized_response()
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)

    session['twitter_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )
    session['twitter_user'] = resp['screen_name']

    return redirect(next_url)


if __name__ == '__main__':
    app.secret_key = ''#TODO: Fill in!
    app.run()


