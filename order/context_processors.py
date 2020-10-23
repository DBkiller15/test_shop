from django.db import connection


def db_queries(request):
    return {'db_connection': connection}
