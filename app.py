from flask import Flask, render_template, request, redirect, url_for, session, flash
from breeze_utils import get_people
from utils import get_birthdays
import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secret key for session management

# Define a route to display birthdays
@app.route('/')
def index():
    if 'user' in session:
        # Get birthdays using your utils.get_birthdays function
        birthdays = get_birthdays_thisweek()
        return render_template('index.html', birthdays=birthdays)
    flash('You need to log in first.', 'error')
    return redirect(url_for('login'))

# Define a route for login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Implement your authentication logic here
        # Example: if username == 'admin' and password == 'password':
        if username == 'admin' and password == 'password':
            session['user'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login failed. Please try again.', 'error')
    return render_template('login.html')

# Define a route for logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

def get_birthdays_thisweek():
    people = get_people(details=1)

    today = datetime.date.today()
    is_sunday = today.weekday() == 6  # Sunday corresponds to 6 in the weekday() method

    # Get birthdays for this week or next week based on whether today is Sunday
    if is_sunday:
        people_with_birthdays = get_birthdays(people)
    people_with_birthdays = get_birthdays(people, next_week=True)
    # this is ugly because I store details in a tuple (details,birthdate)
    return [{'last_name':person[0]['last_name'],'first_name':person[0]['first_name'],"birthdate":format_birthdate(person[1])} for person in people_with_birthdays]

def format_birthdate(birthdate):
    return birthdate.strftime('%B %d')

if __name__ == '__main__':
    app.run(debug=True)


