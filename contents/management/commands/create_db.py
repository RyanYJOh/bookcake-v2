import sys
import logging
import mysql.connector as mc
import os

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

rds_host = os.environ.get("bookcake-lambda.cazdqbj5oijd.ap-northeast-2.rds.amazonaws.com")
# rds_host = os.environ.get("bookcake-db-instance.cazdqbj5oijd.ap-northeast-2.rds.amazonaws.com")
db_name = os.environ.get("bookcake_db_lambda"),
user_name = os.environ.get("ryan")
password = os.environ.get("shris9494")
port = os.environ.get('3690')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class Command(BaseCommand):
    help = 'Creates the initial database'

    def handle(self, *args, **options):
        print('Starting db creation')
        try:
            db = mc.connect(host=rds_host, user=user_name,
            password=password, database="bookcake_db_lambda", connect_timeout=5)
            print('reached here')
            c = db.cursor()
            print("connected to db server")
            c.execute("""CREATE DATABASE bookcake_db;""")
            c.execute("""GRANT ALL ON bookcake_db.* TO 'ryan'@'%'""")
            c.close()
            print("closed db connection")
        except mc.Error as err:
            logger.error("Something went wrong: {}".format(err))
            sys.exit()