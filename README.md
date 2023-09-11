This is the readme
# sundaybreeze

## Quick Start
### Installation
```
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
```
### Running the app
export the environment variables
```
export BREEZE_API_KEY SUBDOMAIN AUTH0_CLIENT_ID AUTH0_CLIENT_SECRET AUTH0_DOMAIN SECRET_KEY  ALLOWED_ACCOUNTS
source .env
```
```
python app.py
```

## Notes

This code requires a valid api key and breeze subdomain which you'll need to provide in an `.env` file
The file will look something like this
```
BREEZE_API_KEY=9419..............
SUBDOMAIN="somethingchapel"
```
~                             
