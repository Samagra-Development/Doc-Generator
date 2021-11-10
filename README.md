# PDF Builder

## Production
Pull the new code and do the following.
```shell
docker-compose down -v
docker-compose -f docker-compose.prod.yml up -d --build
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input --clear
```


## Development Setup
- Create a `.env.dev` file at  `/src/pdf/`
- Create a symlink to the base folder `ln -s ./src/pdf/.env.dev .env`
- Start the DB - `docker-compose up -d db`
- Create a virtual environment for python 3.9. The project is not tested on lower versions.
- Install Dependencies `pip install -r requirements.txt.dev`. Since the requirements.txt is for the production server, it will be finalized later. So please continue using the dev one. Before committing code, always update the file using the following command `pip freeze > requirements.txt.dev`
- Migrate the database `python manage.py migrate`
- Create a superuser `python3 manage.py createsuperuser`
- Start three terminals and run the following commands. These will start `beat`, `worker` and `django` dev server.
    ```shell
    celery --app=pdf.celery.app beat --loglevel=debug --scheduler django_celery_beat.schedulers:DatabaseScheduler
    celery --app=pdf.celery.app worker --loglevel=debug
    python3 manage.py runserver_plus
    ```
- When all is done the following URLs will be available
  - Health Check - http://localhost:8000/ht/?format=json. Make sure everything is up and running.
  - Admin - http://localhost:8000/admin/
- Logging - Logs are all sent on console as well as the Graylog server. Contact the admin if you need Graylog Access.

## Additional Resources 
- Call Recording - https://drive.google.com/file/d/1VKuAifTsidxxIeY8qRTBuLi4PMqNqwhi/view?usp=sharing
