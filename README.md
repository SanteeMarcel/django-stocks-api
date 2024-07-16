## Description

Microservices running through containers using a Django backend.

![Architecture](docker-compose.png)

Explanation video: [Watch here](https://youtu.be/U61AIP_PxLQ)

## Sample Users for Testing

**Super User:**
- Username: `admin`
- Password: `123456`

**Normal User:**
- Username: `peter`
- Password: `spiderman`

## How to Run the Project

1. Ensure you have Docker installed.
2. Use `docker-compose up` at the root of the project directory.
3. Access the application at [http://127.0.0.1:8000/api/schema/swagger-ui/](http://127.0.0.1:8000/api/schema/swagger-ui/).

## How to Run Unit Tests

1. Ensure you have Python 3 installed.
2. Create a virtual environment and activate it:
    ```sh
    python3 -m venv virtualenv
    source virtualenv/bin/activate
    ```
3. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```
4. Run unit tests for each service:
    ```sh
    ./stock_service/manage.py test
    ./api_service/manage.py test
    ```

## How to Use

### Using Swagger

1. Access the Swagger UI at [http://127.0.0.1:8000/api/schema/swagger-ui/](http://127.0.0.1:8000/api/schema/swagger-ui/).
2. Generate a token at `/api/token` using any of the credentials listed above.
3. Insert the token at the "Authorize" button at the top of the Swagger UI.
4. Use the following endpoints:
    - **`/stock`**: Query stock information.
    - **`/history`**: View your query history.
    - **`/stats`**: Check the most queried stocks (requires superuser access).

Your access token lasts 5 minutes. Use the refresh token at `/api/token/refresh` to get a new one.

## Considerations

- PostgreSQL is used due to its popularity. If the `/stock` endpoint is expected to be called much more frequently than `/history` and `/stats`, consider using a NoSQL database for faster writes.
- Logging to the console is fine for debugging, but in production, use robust monitoring tools.
- User credentials and access tokens should never be hardcoded. This is for illustration purposes only. Use a `.env` file for storing secrets.
- Use `autopep8` for code style compliance. 
- Consider using `pika` instead of `celery` for simplicity.
- Use `drf-spectacular` instead of `drf-yasg` due to better support for OpenAPI 3.0 and more frequent updates.

---
