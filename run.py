from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

# from auth_service.app import app

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0')