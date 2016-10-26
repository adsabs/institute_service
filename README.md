Service that currently only implements the maintenance of a database with library link servers. It assumes the existence of a data file containing entries for OpenURL servers (and associated icons). Given an empty database, the tables are created using Alembic.

At the moment the database consists of a table `Institute`, containing data for canonical institutes, and a table `Library`, with data for OpenURL servers, linked to the `Institute` table with an identifier as foreign key.

### updating OpenURL database

The table `Library`, with OpenURL data, is updated by running
```
    python service/manage.py update_openurl
```
which retrieves entries from the file specified in the configuration variable INSTITUTE_OPENURL_DATA and updates the database specified in SQLALCHEMY_DATABASE_URI.
