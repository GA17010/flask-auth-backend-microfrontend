# Flask Auth Backend Microfrontend

This project is a Flask-based backend for authentication and user management. It provides APIs for user registration, login, token-based authentication, and more. The backend is designed to work seamlessly with microfrontend architectures.

## Features

- **User Registration**: Secure user registration with password hashing.
- **User Login**: Authentication with JWT tokens.
- **Token Refresh**: Refresh access tokens using refresh tokens.
- **User Management**: CRUD operations for user data.
- **Password Validation**: Enforces strong password policies.
- **CORS Support**: Configured for cross-origin requests.
- **Database Migrations**: Managed with Alembic.
- **Environment Configuration**: Uses `.env` for sensitive data.
- **Password Recovery**: OTP-based password reset functionality.

## Installation

1. Clone the repository:
  ```bash
  git clone https://github.com/ga17010/flask-auth-backend-microfrontend.git
  cd flask-auth-backend-microfrontend
  ```

2. Create a virtual environment and activate it:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

3. Install dependencies:
  ```bash
  pip3 install -r requirements.txt
  ```

4. Set up the environment variables:
  Create a `.env` file in the root directory with the following content:
  ```env
  SECRET_KEY="your-secret-key"
  DATABASE_URL="your-database-url"
  EMAIL_FROM="your-email@example.com"
  EMAIL_PASSWORD="your-email-password"
  TIME_ZONE="America/El_Salvador"
  ```

5. Run database migrations:
  ```bash
  flask db upgrade
  ```

6. Start the application:
  ```bash
  python3 run.py
  ```

## API Endpoints

### Authentication Routes
- `POST /auth/register`: Register a new user.
- `POST /auth/login`: Login and receive tokens.
- `GET /auth/checkAuth`: Check if the user is authenticated.
- `POST /auth/refreshToken`: Refresh the access token.
- `POST /auth/logout`: Logout and clear tokens.

### User Routes
- `GET /user/users`: Retrieve all users.
- `DELETE /user/users/<id>`: Delete a user by ID.

### Recovery Routes
- `POST /recovery/forgot-password`: Request a password reset OTP.
- `POST /recovery/verify-otp`: Verify the OTP for password reset.
- `POST /recovery/reset-password`: Reset the password using the OTP.

## Project Structure

```
flask-auth-backend-microfrontend/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── models/
│   │   ├── user_model.py
│   │   └── password_reset_token_model.py
│   ├── routes/
│   │   ├── auth_routes.py
│   │   ├── user_routes.py
│   │   └── recovery_routes.py
│   ├── schemas/
│   │   └── user_schema.py
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   └── recovery_service.py
│   ├── utils/
│       ├── jwt_utils.py
│       ├── password_utils.py
│       ├── otp_utils.py
│       └── email_utils.py
├── migrations/
├── requirements.txt
├── run.py
├── wsgi.py
├── Dockerfile
├── docker-compose.yml
└── tests/
   ├── integration/
   │   ├── test_auth.py
   │   └── test_user.py
   ├── postman/
   │   └── Flask_auth_test_backend.postman_collection.json
   └── unitary/
      ├── test_user_schema.py
      ├── test_otp_utils.py
      └── test_jwt_utils.py
```

## License

This project is licensed under the [MIT License](LICENSE).

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## Acknowledgments

- [Flask](https://flask.palletsprojects.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [Flask-Bcrypt](https://flask-bcrypt.readthedocs.io/)
- [Postman](https://www.postman.com/) for API testing.

## Contact

For any inquiries, please contact Gustavo at [gustavoaguirre287@gmail.com].  