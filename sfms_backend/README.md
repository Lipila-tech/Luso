## Language: Python 3.9
## Admin Payment
Logged in staff users can add/remove students to the database and manage their payment information
 <img src="https://github.com/sangwani-coder/portfolio_project/blob/main/images/admin.gif" title="admin panel"></img>
 
## API Endpoints
- api/v1/payments: Accepts POST requests handles students payments and communicates with the MTN API.
- api/v1.history: Accepts GET requests, returns a students transaction history.
- api/v1/login: Accepts POST requests, authenticates a student user.
- api/v1/logout: Accepts POST requests, clears a student users session and logs them out.
- api/v1/logout: GET request, returns a users profile.

## Testing the backend locally
- clone or fork this repo
- create a virtual environment
- pip install requirements.txt
- activate virtual environment
- run python manage.py createsuperuser
Starting the development server
- run python manage.py runserver
- visit localhost to login to admin site
- localhost:8000/admin  

## Testing the hosted (live) backend 
Use the following credentials to [login](https://sfms-backend.herokuapp.com/admin) to the website hosted on [heroku](https:/heroku.com). or copy and paster this link in your browser https://sfms-backend.herokuapp.com/admin
The *passord* for all users is *pwd-admin123*
Both users have superuser status
 - username: mabu, password: pwd-admin123
 - username: chika, password: pwd-admin123
 

