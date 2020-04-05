# Movies GraphQL API

This is a fully fleged GraphQL API built using Python, Django Framework and Postgres as the database engine. It was a lot of fun to explore the Django ORM and the amazing functionalities which it brings with it. My initial choice was to use NodeJs and MongoDB for the backend service but I found it particularly difficult to maintain a ton of many-many relationships (which are really common in the movies world!) in MongoDB and NodeJs also lacks quality SQL ORMS. Which made Python Django my choice for this project. It includes complete CRUD Functionality and focuses on scalable and reusable code. One of the projects I had the most fun creating, it is also live on Heroku! so check it out.

### Change the `.env.example` -> `.env`

## The App is also dockerized!

1. `sudo docker-compose up --build` - This command spins up a **postgres** server (and also the python app, depending on how you configure it. This is done
   so you dont have to install them locally)

2. Install **python 3.6.6** prefferably in a virtual environment

3. `pip install -r requirements.txt` - Installs all the dependencies of the project

4. `./manage.py makemigrations && ./manage.py migrate` - Prepares any migrations (schema change) and then applies then on the database server

5. `./manage.py createsuperuser` - Creates an **admin** user to modify the data. follow the steps the command shows

6. `./manage.py runserver` - Runs the django app on **127.0.0.1:8000**
