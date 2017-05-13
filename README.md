<p align="center"><img src="http://www.azquotes.com/picture-quotes/quote-nothing-in-life-is-to-be-feared-it-is-only-to-be-understood-now-is-the-time-to-understand-marie-curie-6-92-91.jpg"></p>

# Lookformarie

Api to project Lookformarie.


# Quickstart in Development

```
docker-compose up -d
docker-compose run restapi python manage.py migrate
docker-compose run restapi python manage.py createsuperuser
```

Then, django rest framwork will be available at `docker-machine ip [your machine]` on port 8000. 

To create new app:

```
docker-compose run restapi python manage.py startapp my-app project/apps/my-app
```

# Production

Depending on what you use:

```
docker build ./restapi your-app
docker tag your-app tag
docker push your-username/your-app:tag