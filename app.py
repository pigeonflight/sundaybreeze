from flask import Flask, render_template, request, redirect, url_for, session, flash
from authlib.integrations.flask_client import OAuth
#from os import environ as env
from breeze_utils import get_people, get_person, get_profile
from utils import get_birthdays, get_anniversaries
from urllib.parse import quote_plus, urlencode
import datetime
import random
from environs import Env
from flask_caching import Cache

config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}

env = Env()
env.read_env()

app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)
app.secret_key = env("APP_SECRET_KEY")
SUBDOMAIN = env("BREEZE_SUBDOMAIN")


# Configure Auth0
oauth = OAuth(app)
oauth.register(
    "auth0",
    client_id=env("AUTH0_CLIENT_ID"),
    client_secret=env("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env("AUTH0_DOMAIN")}/.well-known/openid-configuration',
)

allowed_accounts = env("ALLOWED_ACCOUNTS").split(',')

from authlib.oauth2 import OAuth2Error

# ...

@app.route('/login')
def login():
    # Generate a random nonce value (use a secure method in production)
    nonce = make_nonce()

    # Save the nonce in the session to use it during callback validation
    session['nonce'] = nonce

    redirect_uri = url_for('callback', _external=True)  # Set the correct callback route

    # Include the nonce in the authorization request
    return oauth.auth0.authorize_redirect(redirect_uri=redirect_uri, nonce=nonce)

# Define a callback route for Auth0
@app.route('/callback')
def callback():
    token = oauth.auth0.authorize_access_token()
    nonce = session.get('nonce')
    user_info = oauth.auth0.parse_id_token(token,nonce)
    session['user_info'] = user_info
    return redirect(url_for('profile'))

@app.route('/apiprofile')
def apiprofile():
    return get_profile()

# Define a profile route
@app.route('/profile')
def profile():
    user_info = session.get('user_info')
    if not user_info:
        return 'Login required'
    if user_info['email'] not in allowed_accounts:
        return f"Your account is not authorised. Ask an admin to authorise {user_info['email']}"
    
    return render_template('profile.html', user_info=user_info)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + env("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("index", _external=True),
                "client_id": env("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

# Define a route to display birthdays
@app.route('/')
def index():
    user_info = session.get('user_info')
    if not user_info:
        return redirect(url_for('login'))
    if user_info['email'] not in allowed_accounts:
        return f"Your account is not authorised. Ask an admin to authorise {user_info['email']}"
    return render_template('index.html')

@app.route('/birthdays')
@cache.cached(timeout=150)
def birthdays():
    user_info = session.get('user_info')
    if not user_info:
        return redirect(url_for('login'))
    if user_info['email'] not in allowed_accounts:
        return f"Your account is not authorised. Ask an admin to authorise {user_info['email']}"
    birthdays = get_birthdays_thisweek()
    return render_template('birthdays.html', birthdays=birthdays)

@app.route('/birthday_gallery')
@cache.cached(timeout=150)
def birthday_gallery():
    user_info = session.get('user_info')
    if not user_info:
        return redirect(url_for('login'))
    if user_info['email'] not in allowed_accounts:
        return f"Your account is not authorised. Ask an admin to authorise {user_info['email']}"
    birthdays = get_birthdays_thisweek()
    return render_template('birthday_gallery.html', birthdays=birthdays)


@app.route('/anniversaries')
@cache.cached(timeout=150)
def anniversaries():
    user_info = session.get('user_info')
    if not user_info:
        return redirect(url_for('login'))
    if user_info['email'] not in allowed_accounts:
        return f"Your account is not authorised. Ask an admin to authorise {user_info['email']}"
    anniversaries = get_anniversaries_thisweek()
    return render_template('anniversaries.html', SUBDOMAIN=SUBDOMAIN, anniversaries=anniversaries)
    return "this is the anniversaries view"
    

@app.route('/person/<id>')
def person(id):
    user_info = session.get('user_info')
    if not user_info:
        return redirect(url_for('login'))
    if user_info['email'] not in allowed_accounts:
        return f"Your account is not authorised. Ask an admin to authorise {user_info['email']}"
    person_info = get_person(id)
    person_info['birthday'] = tobirthday(person_info['details']['birthdate'])
    person_info['notes'] = ""
    if '2065014405' in person_info['details']:
        person_info['notes'] = person_info['details']['2065014405']
    return render_template('person.html', person_info=person_info)


def tobirthday(input_date):
    """ takes a date in the format YYYY-MM-DD and converts it the someone's birth date for this year"""

    current_year = datetime.datetime.now().year

    # Replace the first 4 digits with the current year
    birthday_date = f"{current_year}{input_date[4:]}"
    parsed_date = datetime.datetime.strptime(birthday_date, "%Y-%m-%d")

    # Format the parsed date as "Month Day" (e.g., "September 10")
    formatted_date = parsed_date.strftime("%B %d")

    return formatted_date

import datetime

def get_anniversaries_thisweek():
    people = get_people(details=1)  # Assuming you have a 'get_people' function
    today = datetime.date.today()
    is_sunday = today.weekday() == 6  # Sunday corresponds to 6 in the weekday() method

    # Get anniversaries for this week or next week based on whether today is Sunday
    if is_sunday:
        anniversaries = get_anniversaries(people)
    else:
        anniversaries = get_anniversaries(people, next_week=True)

    formatted_anniversaries = []

    for person, anniversary_date in anniversaries:
        formatted_anniversaries.append({
            'last_name': person['last_name'],
            'id': person['id'],
            'first_name': person['first_name'],
            'path': person['path'],
            'anniversary_date': format_to_month_and_day(anniversary_date),
            'details': person.get('details', {}),
        })

    return formatted_anniversaries


def get_birthdays_thisweek():
    people = get_people(details=1)
    today = datetime.date.today()
    is_sunday = today.weekday() == 6  # Sunday corresponds to 6 in the weekday() method

    # Get birthdays for this week or next week based on whether today is Sunday
    if is_sunday:
        people_with_birthdays = get_birthdays(people)
    else:
        people_with_birthdays = get_birthdays(people, next_week=True)
    # this is ugly because I store details in a tuple (details,birthdate)
    return [{'last_name':person[0]['last_name'],
             'id':person[0]['id'],
             'first_name':person[0]['first_name'],
             'path':person[0]['path'],
             'birthdate':format_to_month_and_day(person[1]),
             'details':person[0]['details']}  for person in people_with_birthdays]

def format_to_month_and_day(birthdate):
    return birthdate.strftime('%B %d')

def make_nonce():
    """Generate pseudorandom number."""
    return str(random.randint(0, 100000000))


if __name__ == '__main__':
    app.run(debug=True)
