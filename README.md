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

## Usage

    git clone git@github.com:sangwani-coder/lipila-dot-tech.git
    cd lipila-dot-tech    
    python -m .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    
    cd lipila

    python manage.py migrate
    python manage.py runserver


## Contribution

1. Fork the repository.
2. Create a new branch for your changes.
3. Make changes and commit them.
4. Submit a pull request.