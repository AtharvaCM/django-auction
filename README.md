# django-auction

An auction project with django as a backend.

### command to migrate sqlite to psql

pgloader <path_of_sqlite_file> postgresql:///<dbname>

### command to reset heroku db

heroku pg:reset <db_add_on_name> --app <appname>

### command to push local db to heroku db

heroku pg:push <local_db_name> <db_add_on_name> -app <appname>
