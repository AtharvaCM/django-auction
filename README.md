# django-auction

An auction project with django as a backend.

This repo contains the source code, documentation and ppt for this project.

If you wish to use this project please change the SMTP and email credentials and add your own.

### command to migrate sqlite to psql

pgloader <path_of_sqlite_file> postgresql:///<db_name>

### command to reset heroku db

heroku pg:reset <db_add_on_name> --app <app_name>

### command to push local db to heroku db

heroku pg:push <local_db_name> <db_add_on_name> -app <app_name>
