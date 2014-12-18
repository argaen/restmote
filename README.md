# Django restmote

This package allows to synchronize a local database pulling data from a REST API. To populate the local database, Django ORM is used.

### Populate a local database from a remote one. The database already existed and wasn't build with Django. The script to sync external data is out from the Django project.

First, we need to define our models so restmote can work with them. To do so, Django provides us an awesome management command: `inspectdb`. So, let's build our Django models:

1. Build our project: `django_admin startproject project`
2. `cd project/project` and edit the _settings.py_ file. Set the database variables so you can access it (NAME, BACKEND, PORT, etc.).
3. Once set, execute the `python manage.py inspectdb` command. It will print lots of stuff (your models). If the commands throws an error, check your database variables are correct.
4. If the command worked, create a new application `python manage.py startapp app`.
5. Do `python manage.py inspectdb > app/models.py`

With this, you will have your models defined in your Django app. To check it is working do `python manage.py shell` and then try to import your models with `from app.models import Model1`. You can also check to obtain all the objects with `Model1.objects.all()`.


Having the previous steps, we now need to define some variables in our `project/project/settings.py` file:

* RESMOTE_HOST: Host where the API REST is serving the data. Ex: 'https://api.github.com/'
* RESMOTE_PORT: Port where the API REST is serving. Ex: '80'
* RESTMOTE_API_ROOT: Root of the API in the server. Just in case the API ROOT is different from the HOST.
* RESTMOTE_FILTER_FIELD: File to filter data [to improve].
* RESTMOTE_SNAP_FILE: File to store the last filter [we use date filtering now with last_modified field for the content, to improve].


With those variables defined, we can now create a script (anywhere) that will collect data from the external API and save it in our local database:


    import sys
    import django
    import os

    sys.path.append("/path/to/project/project")
    os.environ["DJANGO_SETTINGS_MODULE"] = "project.settings"
    django.setup()
    from contents.models import GithubUser
    from restmote.sync import sync_objects


    githubuser_field_bindings = {
        'login': 'field1',
        'avatar_url': 'field2',
    }

    sync_objects("/users", Model1, "githubuser", githubuser_field_bindings)


With this code we would pull github users to our local database and create new instances with 'field1' and 'field2' columns being the 'login' and the 'avatar_url' respectively (you can change the bindings according to your column models).

The "githubuser" string is used to build the id, this will change in future versions so you can specify remote id and local id for each model.

Now you can call this script periodically (using cron) to synchronize your models according to their 'last_modified' field.
