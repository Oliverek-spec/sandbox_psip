import sqlalchemy
import psycopg2
db_params = sqlalchemy.URL.create(
    drivername = "postgresql",
    username = 'postgres',
    password = '15082000',
    host = 'localhost',
    database = 'postgres',
    port = 5433
)
engine = sqlalchemy.create_engine(db_params)
connection = engine.connect()
sql_query_1 = sqlalchemy.text("INSERT INTO public.test_table(name) VALUES ('Stanisław');")
connection.execute(sql_query_1)