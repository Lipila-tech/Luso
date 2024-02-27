# Lipila

**Overview**

- Allows remote collection of fees via mobile money
- Allows disbursement of funds to multiple users

## Local machine usage
Ensure you have python 3 installed
[Download it here](https://www.python.org/downloads/)

    git clone git@github.com:your-username/lipila-dot-tech.git

    cd lipila-dot-tech    

    python -m .venv

    source .venv/bin/activate <!-- Linux -->

    .venv/scripts/activate <!-- Windows -->

    pip install -r requirements.txt
    

    cd lipila

    <!-- *Copy and set your environment variables in the .env file.* -->

    cp backend/example.env backend/.env

    python manage.py migrate
    python manage.py runserver

Access your Web App at:

localhost:8000/

[more](./lipila/web/)


Access the Django Rest API Root at:

localhost:8000/api/v1/

[more](./lipila/api/)


**API Keys COnfiguration**

- Register to use the MTN momo api at
    
    https://momodeveloper.mtn.com

Once you subscribe to a product copy the keys and add in your .env file.


**Testing**

api Code:
    python -m manage.py test api.tests

web app Code:
    python -m manage.py test api.tests


**Contributing**

1. Fork the repository[lipila-dot-tech](https://github.com/Lipila-tech/Lipila-rest-api)
2. Create a new branch for your changes. [see branching](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell)
3. Make changes and commit them.
4. Submit a pull request.[See making a pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request)
-

**License**

-

**Contact**

zyambopeter1@gmail.com
