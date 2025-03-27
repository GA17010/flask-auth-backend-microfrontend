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

## Project Structure

```
flask-auth-backend-microfrontend/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── models/
│   │   └── user_model.py
│   ├── routes/
│   │   ├── auth_routes.py
│   │   └── user_routes.py
│   ├── schemas/
│   │   └── user_schema.py
│   ├── services/
│   │   ├── auth_service.py
│   │   └── user_service.py
│   ├── utils/
│       ├── jwt_utils.py
│       └── password_utils.py
├── migrations/
├── requirements.txt
├── run.py
└── wsgi.py
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

## Contact

For any inquiries, please contact Gustavo at [gustavoaguirre287@gmail.com].  