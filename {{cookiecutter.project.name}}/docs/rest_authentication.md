# Django Rest Auth

## Features
- User Registration with activation
- Login/Logout
- Retrieve/Update the Django User model
- Password change
- Password reset via e-mail


## API endpoints

### Basic
- `/auth/login/ (POST)`

  - username
  - email
  - password
  
  Returns Token key

- `/auth/logout/ (POST)`

- `/auth/password/reset/ (POST)`

    - email

- `/auth/password/reset/confirm/ (POST)`

    - uid
    - token
    - new_password1
    - new_password2

- `/auth/password/change/ (POST)`

    - new_password1
    - new_password2
    - old_password

- `/auth/user/ (GET, PUT, PATCH)`

    - username
    - first_name
    - last_name

    Returns pk, username, email, first_name, last_name

- `/auth/token/verify/ (POST)`

    - token

    Returns an empty JSON object.

- `/auth/token/refresh/ (POST)` ([see also](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html#usage))

    - refresh

  Returns access

### Registration

- `/auth/registration/ (POST)`

    - username
    - password1
    - password2
    - email

- `/auth/registration/verify-email/ (POST)`

    - key

- `/auth/registration/resend-email/ (POST)`

    - email

    Resends the email verification