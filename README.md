# Django_token_authentication

# Introduction

Custom Django middleware for token based authentication



It implements the following functionalities:

    
 1.Creates a token after the user login's \
 2.Then the user is provided with the token (via some medium)(for now terminal) \
 3.The user needs to type in the token as directed on the page to watch special functionalities on the webpage \
 4.At the time token is created a expiry time of the token is also set. This can be changed in basic_pr/settings.py by the changing the seconds in \
   EXPIRING_TOKEN_DURATION= timedelta(seconds=600) \
 5.Tokens expires after the set time and if user clicks anywhere on the page then user is logged out and told to login in again \
 6.After the token expiry,the session is also expired and so the user is logged out of the webpage \
 7.If the user is logs in again then a new token is generated for the user.
    
# Quick setup
  
  Requirements:
  
  Python-3.6 \
  pip3 install -r requirements.txt
  
  Go to the directory where Django_token_authentication downloaded
  
  python manage.py makemigrations \
  python manage.py migrate \
  python manage.py runserver
  
  Then go to the browser and enter the url http://127.0.0.1:8000/
  
# Login or Register

  You can access the django admin page at http://127.0.0.1:8000/admin by creating admin user i.e the superuser
  
  Also a new admin user can be created using  
  python manage.py createsuperuser

  For a normal user which is not a superuser, login and register can be done on the webpage itself.
  
  For viewing extra additional details regarding the webpage the user needs to login and authenticate his token.
  
 
  