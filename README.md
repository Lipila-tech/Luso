# Lipila-ui

## Overview

Lipila-ui provides a user-friendly interface for sending money using mobile money. Key features include:

- **Streamlined payment form:** Collects payment details efficiently in 1 step.
- **Intuitive interactions:** Simple form fields guide users through the process.
- **Confirmation and security:** Ensures payment details are accurate and secure.


## Navigation

Users navigate through the payment process sequentially:

1. InformationEntryFields
2. Confirmation (after form submission)

## User Interactions

- Fill in required form fields.
- Navigate between steps using buttons.
- Confirm payment with PIN on user phone.


## Contribution

1. Fork the repository[(lipila-dot-tech](https://github.com/Lipila-tech/Lipila-rest-api)
2. Create a new branch for your changes. [see branching](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell)
3. Make changes and commit them.
4. Submit a pull request.[See making a pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request)

## Usage on Your local machine
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

Access your website at:

    localhost:8000/api/v1/index


Access the Django Rest API Root at:

    Access your website at:

    localhost:8000/api/v1/

### Admin section:

    localhost:8000/admin

    username: sangwa
    password: test@123

### Testing sellers ID's:

- pita
- zyambo
- sangwani
- sangwa - failing(this is a superuser)
