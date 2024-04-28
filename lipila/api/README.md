# API

## API Usage on Your local machine

## Root
_Api Root: GET /lipila/api/v1/_

Returns all availabel endpoints.

Response:

    HTTP 200 OK
    Allow: GET, HEAD, OPTIONS
    Content-Type: application/json
    Vary: Accept

   {
        "payments": "http://localhost:8000/api/v1/payments/",
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
    "account_number": "",
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

## Payments
_GET /payments/?payee=<username>/_

### Response
#### OK
*Status Code* 200

*Response Body:*

[
    {
        "payee": 1,
        "payer_account": "0965604023",
        "amount": "4555.00",
        "timestamp": "2024-02-25T08:10:13.601683Z",
        "description": "Piano lessons",
        "payer_email": "test@bot.com",
        "payer_name": "Xanthe"
    },
    {
        "payee": 1,
        "payer_account": "0971892260",
        "amount": "444.00",
        "timestamp": "2024-02-25T08:11:37.413323Z",
        "description": "Karate lessons",
        "payer_email": "sangw@bot.com",
        "payer_name": "Xanthe"
    }
]

_POST_ /payments/_

### Request Body:

{
    "payee": null,
    "payer_account": "",
    "amount": null,
    "description": "",
    "payer_email": "",
    "payer_name": ""
}

*Status Code* 201

*Response Body:*

{
    "message": "OK"
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
