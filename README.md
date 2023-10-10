This is the readme
# sundaybreeze
Birthday and Anniversary Dashboard for the Breeze ChMS

![screenshot](sbreeze.jpg)

## Quick Start
### Installation
```
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
```
### Running the app
```
python app.py
```

## Notes

This code requires a valid api key and breeze subdomain which you'll need to provide in an `.env` file
The file will look something like this
```
BREEZE_API_KEY=9419..............
SUBDOMAIN="somethingchurch"
AUTH0_CLIENT_ID=rxxxxxxxxxxxxxxxxxxxxxxxxxxx....
AUTH0_CLIENT_SECRET=_6du.................................Z6lt-
AUTH0_DOMAIN=.........................auth0.com
# set a long secret key
SECRET_KEY=342............DFASFDAFewre
ALLOWED_ACCOUNTS="john@example.com,marylamb@example.com"
```
