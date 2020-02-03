from conf import settings
import asyncpg
import json
import psycopg2


async def get_connection_async():
    cnx = await asyncpg.connect(
        host=settings.DATABASE.PGHOST,
        database=settings.DATABASE.PGDBNAME,
        user=settings.DATABASE.PGUSER,
        password=settings.DATABASE.PGPASSWORD,
        port=settings.DATABASE.PGPORT
    )
    await cnx.set_type_codec("jsonb", encoder=json.dumps, decoder=json.loads, schema="pg_catalog")
    await cnx.set_type_codec("json", encoder=json.dumps, decoder=json.loads, schema="pg_catalog")
    return cnx


def get_connection():
    cnx = psycopg2.connect(
        host=settings.DATABASE.PGHOST,
        dbname=settings.DATABASE.PGDBNAME,
        user=settings.DATABASE.PGUSER,
        password=settings.DATABASE.PGPASSWORD,
        port=settings.DATABASE.PGPORT
        )
    return cnx