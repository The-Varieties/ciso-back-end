# Getting started for the Backend Side
* Make sure install the Django first: `pip install Django==4.0.3`
* If there is some changes to the database then you might need to migrate first: `python manage.py migrate`
* To run the server for the Django server: `python manage.py runserver`

# Getting started for running the Prometheus + Target Instance + Database (PostgreSQL and Promscale)
* First make sure download docker first
* Next, from your terminal, make sure you are the same level or inside the directory which contains **docker-compose.yml** file
* Then, just run `docker-compose up`
* To stop, run `docker-compose down`

**WARNING: These docker will consume your RAM usage so make sure to allocate some for this**
