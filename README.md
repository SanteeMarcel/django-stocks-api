# Python/Django Challenge

super user:
user = admin
password = 123456

normal user:
user = peter
password = spiderman

## How to run the project
* Ensure you have python3 installed.
* Create a virtualenv: `python3 -m venv virtualenv` and activate it `. virtualenv/bin/activate`.
* Install dependencies: `pip install -r requirements.txt`
* Run migrations and start api service: `cd api_service ; python3 manage.py migrate; ./manage.py runserver 8000`
* Start the stock service: `cd stock_service ; ./manage.py runserver 8001`


# How to Use

**Using Swagger**

Access http://127.0.0.1:8000/api/schema/swagger-ui/

Generate a token at /api/token and any of the credentials listed above.
Insert the token at "Authorize" at the top.
Use the "/stock" endpoint to query stock.
Use the "/history" endpoint to see your own query history.
Use the "/stats" endpoint to check up the most queried stocks, requires superuser.

Your access token only lasts 5 minutes, use your refresh token at /api/token/refresh to get a new one.

**Commands below using curl**

`curl -X POST http://127.0.0.1:8000/api/token/ -d "username=peter" -d "password=spiderman"`

This will return two tokens, Access and Refresh. Use Access as a header for all endpoints. Like this:

`curl -X GET "http://127.0.0.1:8000/stock?stock_code=aapl.us" -H "Authorization: Bearer <access_token>"`

Your access token expires in five minutes, so if you need obtain another, use the refresh token:

`curl -X POST http://127.0.0.1:8000/api/token/refresh/ -d "refresh=<refresh_token>"`

`curl -X GET "http://127.0.0.1:8000/stock?stock_code=aapl.us" -H "Authorization: Bearer <access_token>"`

`curl -X GET http://127.0.0.1:8000/history -H "Authorization: Bearer <access_token>"`

`curl -X GET http://127.0.0.1:8000/stats -H "Authorization: Bearer <access_token>"` // must be superuser

Disclaimer: The access token only lasts 5 minutes!

# Considerations

sqlite is not suitable for production, I would probably use a nosql database for faster writes, or a more suitable SQL vendor for faster reads of aggregate data.

The database should never be running alongside the application layer, this is for illustrative purposes only.

Logging to console is fine for debugging purposes, but in production it's better to have more robust monitoring tools.

User credentials and access tokens should never be hardcoded, this is also for illustration purposes only.
