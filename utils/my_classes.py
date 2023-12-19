import sqlalchemy
from dotenv import load_dotenv
import os
from sqlalchemy import orm
import geoalchemy2
load_dotenv()
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
connection.commit()

Base = orm.declarative_base()
class User(Base):
    __tablename__ = 'test_table1'
    id = sqlalchemy.Column(sqlalchemy.Integer(), primary_key=True)
    imię = sqlalchemy.Column(sqlalchemy.String(100), nullable=True)
    nick = sqlalchemy.Column(sqlalchemy.String(100), nullable=True)
    miasto = sqlalchemy.Column(sqlalchemy.String(100), nullable=True)
    posty = sqlalchemy.Column(sqlalchemy.Integer(), nullable=True)
    
inspector = sqlalchemy.inspect(engine)
if User.__tablename__ not in inspector.get_table_names():
    Base.metadata.create_all(engine)
    
Session = orm.sessionmaker(bind=engine)
session = Session()
#CREATE->INSERT
def nick_add():
    while True:
        nickname = input('Podaj nick ')
        nick_check = session.query(User).filter(User.nick == nickname).all()
        if len(nick_check) != 0:
            print('Nick zajęty')
        else:
            return nickname
def add_user():
    name_to_add = input('Podaj imię ')
    nick_to_add = nick_add()       
    posts_to_add = input('Podaj ilość postów ')
    city_to_add = input('Podaj miasto ')
    obiekt_do_dodania = User(
        imię=name_to_add,
        nick=nick_to_add,
        miasto=city_to_add,
        posty=int(posts_to_add) 
    )
    session.add(obiekt_do_dodania)


#READ->SELECT
def show_users_list():
    users = session.query(User).all()
    if users == None:
        print('Brak użytkowników do wyświetlenia')
    print('Lista użytkownków:')
    for user in users:
        print(f'Użytkownik {user.nick} ma na imię {user.imię}, wysłał {user.posty} posty i mieszka w miejscowości {user.miasto}')
show_users_list()
#UPDATE->
def update_user():
    user_to_update= input('Podaj nick użytkownika, który ma zostać zmodyfikowany ')
    user= session.query(User).filter(User.nick == user_to_update).first()
    if user is None:
        print('Nie ma użytkownika o takim nicku')
    elif user.nick == user_to_update:
        new_name = input('Podaj nowe imię ')
        if new_name != "":
            user.imię = new_name
        user.nick = nick_add()
        new_city = input('Podaj nowe miasto ')
        if new_city != "":
            user.miasto = new_city
        new_posts = input('Podaj nową ilość postów ')
        if new_posts != "":
            user.posty = int(new_posts)

#DELETE 
def delete_user():
    user_to_delete = input('Podaj nick użytkownika, który ma zostać usunięty ')
    user= session.query(User).filter(User.nick == user_to_delete).first()
    if user is None:
        print('Nie ma użytkownika o takim nicku')
    elif user.nick == user_to_delete:
        session.delete(user)

session.commit()
session.flush()
connection.close()
engine.dispose()