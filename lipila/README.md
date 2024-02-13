# Payment App Api

**Overview**

- Allows remote collection of fees via mobile money
- Allows disbursement of funds to multiple users

**Installation**

    clone this repo git@github.com:sangwani-coder/lipila-dot-tech.git

    cd lipila-dot-tech

    python -m venv .venv

    source .venv/bin/activate
    
    pip install -r requirements.txt

copy the example.env file to .env and set the environment variables

**API Key COnfiguration**

- Register to use the MTN mom api at
    
    https://momodeveloper.mtn.com

Once you subscribe to a product copy the keys and add in your .env file.

**Usage**

    cd backend

    python -m manage runserver

**Testing**

    python -m manage.py test api.tests

**API Reference**

_Api Root: GET /lipila/api/v1/_

Returns all avalabel endpoints.

Response:

    HTTP 200 OK
    Allow: GET, HEAD, OPTIONS
    Content-Type: application/json
    Vary: Accept

    {
        "student": "http://localhost:8000/lipila/api/v1/student/",
        "parent": "http://localhost:8000/lipila/api/v1/parent/",
        "payment": "http://localhost:8000/lipila/api/v1/payment/",
        "school": "http://localhost:8000/lipila/api/v1/school/",
        "lipila-payment": "http://localhost:8000/lipila/api/v1/lipila-payment/",
        "profile": "http://localhost:8000/lipila/api/v1/profile/"
    }

**Contributing**

-

**License**

-

**Contact**

zyambopeter1@gmail.com
