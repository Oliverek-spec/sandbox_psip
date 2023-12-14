import sqlalchemy
from dotenv import load_dotenv
import os
from sqlalchemy import orm
import geoalchemy2
load_dotenv()
db_params = sqlalchemy.URL.create(
    drivername = "postgresql",
    username = 'postgres',#os.getenv('POSTGRES_USER'),
    password = '15082000',#os.getenv('POSTGRES_PASSWORD'),
    host = 'localhost',#os.getenv('POSTGRES_HOST'),
    database = 'postgres',#os.getenv('POSTGRES_DATABASE'),
    port = 5433 #os.getenv('POSTGRES_PORT')
)
engine = sqlalchemy.create_engine(db_params)
connection = engine.connect()
#sql_query_1 = sqlalchemy.text("INSERT INTO public.test_table(name) VALUES ('Maciej');")
#connection.execute(sql_query_1)
connection.commit()

Base = orm.declarative_base()
class User(Base):
    __tablename__ = 'mytable'
    id = sqlalchemy.Column(sqlalchemy.Integer(), primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(100), nullable=True)
    location = sqlalchemy.Column('geom', geoalchemy2.Geometry(geometry_type='POINT',srid=4326),nullable=True)
Base.metadata.create_all(engine)

#CREATE->INSERT
Session = orm.sessionmaker(bind=engine)
session = Session()
# obiekt_do_dodania = User(
#     name='Oliver',
#     location='POINT(52 18)'
# )
# session.add(obiekt_do_dodania)


#READ->SELECT
users_from_db = session.query(User).all()
for user in users_from_db:
    print(user)

#UPDATE->
users_from_db = session.query(User).all()
for user in users_from_db:
    if user.name == 'Oliver':
        user.name = 'Stanisław'
        
session.commit()
session.flush()
connection.close()
engine.dispose()