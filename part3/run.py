from app import create_app
from app.services.facade import facade

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        if not facade.get_user_by_email("john.doe@example.com"):
            facade.create_user({
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "password": "1234",
                "is_admin": False
            })
            print("User created : john.doe@example.com / 1234")

    app.run(debug=True)
