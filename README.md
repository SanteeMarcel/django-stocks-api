# Python/Django Challenge

super user:
user = admin
password = 123456

normal user:
user = peter
password = spiderman

## How to run the project
* Create a virtualenv: `python -m venv virtualenv` and activate it `. virtualenv/bin/activate`.
* Install dependencies: `pip install -r requirements.txt`
* Start the api service: `cd api_service ; ./manage.py runserver 8000`
* Start the stock service: `cd stock_service ; ./manage.py runserver 8001`


# How to Use

**Commands below using httpie**

`http post http://127.0.0.1:8000/api/token/ username=peter password=spiderman`

This will return two tokens, Access and Refresh. Use Access as a header for all endpoints. Like this:

`http post http://127.0.0.1:8000/stock "Authorization: Bearer <access_token here>"  stock_code=aapl.us`

Your access token expires in five minutes, so if you need obtain another, use the refesh token:

`http post http://127.0.0.1:8000/api/token/refresh/ refresh=<refresh_token here>`

`http get http://127.0.0.1:8000/stock "Bearer Token <access_token here>" stock_code = aapl.us`

`http get http://127.0.0.1:8000/history "Bearer Token <access_token here>"`

`http get http://127.0.0.1:8000/stats "Bearer Token <access_token here>"` // must be superuser

Disclaimer: The access token only lasts 5 minutes!
