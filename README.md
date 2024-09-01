# TravelBuddyBackend

## Prerequisites
- Python vs 3.12
- Postgresql 

## Installation and execution

1. **Fork the repository**

   Open the repository [TravelBuddyBack](https://github.com/jess-ar/TravelBuddyBack.git) in GitHub and click the "Fork" button located in the upper right corner of the page. It creates a copy of our repository in your own Github account.


2. **Clone your forked repository**

   Open a Git Bash terminal and run the command with the link to your new repository:

```bash
# Clone this repository 

```

3. **In Pycharm, open the directory you've just cloned**


4. **Create the virtual environment and then activate it**

```bash
# Create the virtual environment

python -m venv venv

# Activate the virtual environment

venv\Scripts\activate

#And if you need to deactivate the virtual environment

venv\Scripts\deactivate

```

5. **Continue with the following installations**
```bash
#Install all the Python packages listed in the file requirements.txt.

pip install -r requirements.txt

#Install the djangorestframework-simplejwt package.This package provides JSON Web Token (JWT) authentication
#for Django REST Framework (DRF):

pip install djangorestframework-simplejwt

#Displays information about the djangorestframework package installed in your environment

pip show djangorestframework

#Start the Django development server:

python manage.py runserver

#Install the django-cors-headers package, an app that allows you to handle CORS(Cross-Origin Resource Sharing)in your
#Django application:

pip install django-cors-headers

#Once installed, you can add it to your Django project's INSTALLED_APPS and configure it in settings.py to manage CORS.

#Install the psycopg2-binary package. It's the most popular PostgreSQL database adapter for Pythonthat allows your Django
#application to interact with a PostgreSQL database:

pip install psycopg2-binary

#After installation, update the DATABASES setting in settings.py.

#Finally, type these commands in your terminal to manage database changes in your Django project:

python manage.py makemigrations
python manage.py migrate

```

6. **Create your branch and start working!**

```bash
#Create your branch

git checkout -b feature/yourbranchname
```

## Structure documentation

Users interact with the frontend website and call this API, which uses a PostgreSQL database to store data. 

Configuration variables and cached files should be added to `.gitignore` so they are not tracked:

	.env
	__pycache__/
