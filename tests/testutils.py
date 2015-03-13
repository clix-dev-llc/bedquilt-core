import psycopg2
import os
import getpass


# CREATE DATABASE bedquilt_test
#   WITH OWNER = {{owner}}
#        ENCODING = 'UTF8'
#        TABLESPACE = pg_default
#        LC_COLLATE = 'en_GB.UTF-8'
#        LC_CTYPE = 'en_GB.UTF-8'
#        CONNECTION LIMIT = -1;


def get_pg_connection():
    return psycopg2.connect(
        "dbname=bedquilt_test user={}".format(getpass.getuser())
    )
