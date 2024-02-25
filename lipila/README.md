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

## Root
_Api Root: GET /lipila/api/v1/_

Returns all availabel endpoints.

Response:

    HTTP 200 OK
    Allow: GET, HEAD, OPTIONS
    Content-Type: application/json
    Vary: Accept

    {
        "lipila-payment": "http://localhost:8000/api/v1/lipila-payment/",
        "user-transactions": "http://localhost:8000/api/v1/user-transactions/",
        "products": "http://localhost:8000/api/v1/products/",
        "signup": "http://localhost:8000/api/v1/signup/",
        "profile": "http://localhost:8000/api/v1/profile/"
    }

## Signup
_Signup: POST /signup/_

### Request Body:

{
    "username": "", 
    "email": "",
    "password": "",
    "phone_number": "",
    "bio": ""
}

### Response

#### OK
 *Status Code:* 201

 *Response Body:*
{
    "message": "Created"
}

#### Error
*Bad Request*
*Status Code:* 400

*Resonse Body*
{
    "Error": "Failed to signup"
}

## Products
_GET /products/?user=<username>/_

### Response
#### OK
*Status Code* 200

*Response Body:*

[
    {
        "id": 1,
        "product_name": "Piano lesson",
        "price": 150.0,
        "date_created": "2024-02-25T07:08:41.750854Z",
        "status": true,
        "product_owner": 1
    }
]


_POST_ /products/_

### Request Body:

{
    "product_name": "",
    "price": null,
    "status": false,
    "product_owner": null
}

*Status Code* 201

*Response Body:*

{
    "id": 2,
    "product_name": "Karate Class",
    "price": 350.0,
    "date_created": "2024-02-25T07:28:25.555253Z",
    "status": true,
    "product_owner": 3
}

**Contributing**

-

**License**

-

**Contact**

zyambopeter1@gmail.com
