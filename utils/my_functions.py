import requests
import folium
import sqlalchemy
import os
import geoalchemy2
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from sqlalchemy import orm
from my_classes import User



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
# class User(Base):
#     __tablename__ = 'test_table1'
#     id = sqlalchemy.Column(sqlalchemy.Integer(), primary_key=True)
#     imię = sqlalchemy.Column(sqlalchemy.String(100), nullable=True)
#     nick = sqlalchemy.Column(sqlalchemy.String(100), nullable=True)
#     miasto = sqlalchemy.Column(sqlalchemy.String(100), nullable=True)
#     posty = sqlalchemy.Column(sqlalchemy.Integer(), nullable=True)
    
inspector = sqlalchemy.inspect(engine)
if User.__tablename__ not in inspector.get_table_names():
    Base.metadata.create_all(engine)
Session = orm.sessionmaker(bind=engine)
session = Session()

def menu():
    while True:
        print('Witaj')
        #Dodaj
        print('Naciśnij [1] aby dodać użytkownika' )
        #Wyswietl
        print('Naciśnij [2] aby wyświetlić listę użytkowników' )
        #Zmien
        print('Naciśnij [3] aby zmienić dane użytkownika' )
        #Usun
        print('Naciśnij [4] aby usunąć użytkownika' )
        #Generator map
        print('Naciśnij [5] aby przejść do generatora map' )
        #Zakończ
        print('Naciśnij [0] aby zakończyć program' )

        choice = input('Wybierz funkcję do wykonania ')
        match choice :
            case '1':    
                add_user()
            case '2':   
                show_users_list()
            case '3':
                update_user()
            case '4':   
                delete_user()
            case '5':
                map_menu()
            case '0':  
                print('Do zobaczenia!')
                session.commit()
                connection.close()
                engine.dispose() 
                return
            case _:
                print('To nie jest funkcja! Proszę wybierz funkcję z zakresu 0-5')
            
def map_menu():
    while True:
        #Wyświetl miejscowośi wszystkich użytkowników
        print('Naciśnij [1] aby wyświetlić miejscowości wszystkich użytkowników' )
        #Wyświetl miejscowość jednego użytkownika
        print('Naciśnij [2] aby wyświetlić miejscowość jednego użytkownika' )
        #Powrót
        print('Naciśnij [0] aby wrócić do menu' )
        map_choice = input('Wybierz funkcję do wykonania ')
        match map_choice:
            case '1':
                get_map_of_all()
            case '2':
                get_map_of_one()
            case '0':
                return
            case _:
                print('To nie jest funkcja! Proszę wybierz funkcję z zakresu 0-2')
            
    
def nick_checker():
    while True:
        nickname = input('Podaj nick ')
        nick_check = session.query(User).filter(User.nick == nickname).all()
        if len(nick_check) != 0:
            print('Nick zajęty')
        if nickname == '':
            print('Nick musi zawierać znaki')
        else:
            return nickname
def add_user():
    name_to_add = input('Podaj imię ')
    nick_to_add = nick_checker()       
    posts_to_add = input('Podaj ilość postów ')
    city_to_add = input('Podaj miasto ')
    obiekt_do_dodania = User(
        imię=name_to_add,
        nick=nick_to_add,
        miasto=city_to_add,
        posty=int(posts_to_add) 
    )
    session.add(obiekt_do_dodania)
    session.commit()
def show_users_list():
    users = session.query(User).all()
    if users == None:
        print('Brak użytkowników do wyświetlenia')
    print('Lista użytkownków:')
    for user in users:
        print(f'Użytkownik {user.nick} ma na imię {user.imię}, wysłał {user.posty} posty i mieszka w miejscowości {user.miasto}')
    session.commit()
def update_user():
    user_to_update= input('Podaj nick użytkownika, który ma zostać zmodyfikowany ')
    user= session.query(User).filter(User.nick == user_to_update).first()
    if user is None:
        print('Nie ma użytkownika o takim nicku')
    elif user.nick == user_to_update:
        new_name = input('Podaj nowe imię ')
        if new_name != "":
            user.imię = new_name
        user.nick = nick_checker()
        new_city = input('Podaj nowe miasto ')
        if new_city != "":
            user.miasto = new_city
        new_posts = input('Podaj nową ilość postów ')
        if new_posts != "":
            user.posty = int(new_posts)
    session.commit()
def delete_user():
    user_to_delete = input('Podaj nick użytkownika, który ma zostać usunięty ')
    user= session.query(User).filter(User.nick == user_to_delete).first()
    if user is None:
        print('Nie ma użytkownika o takim nicku')
    elif user.nick == user_to_delete:
        session.delete(user)
    session.commit()
def get_coordinates_of(city:str)->list[float,float]:
    adres_URL = f'https://pl.wikipedia.org/wiki/{city}'
    response = requests.get(url=adres_URL)
    response_html = BeautifulSoup(response.text, 'html.parser')
    latitude = response_html.select('.latitude')[1].text
    longitude = response_html.select('.longitude')[1].text
    latitude_flt = float(latitude.replace(',','.'))
    longitude_flt = float(longitude.replace(',','.'))
    return [latitude_flt, longitude_flt]

def get_map_of_all()->None: 
    map = folium.Map(
        location = [52.5, 19],  
        titles='OpesStreetMap', 
        zoom_start=6)
    users = session.query(User).all()
    if users == None:
        print('Brak użytkowników do wyświetlenia')
    else:
        for user in users:
            folium.Marker(
                location= get_coordinates_of(user.miasto), 
                popup=f'{user.miasto} tu mieszka {user.nick} ma na imię {user.imię} i wysłał {user.posty} posty'
                ).add_to(map)
        map.save(f'mapka.html')
        print('Mapa wszystkich użytkowników pomyślnie wygenerowana :)')
    session.commit()
    
def get_map_of_one()->None:
    user_to_map = input('Podaj nick użytkownika, którego mapa ma zostać wyświetlona ')
    user= session.query(User).filter(User.nick == user_to_map).first()
    if user is None:
        print('Nie ma użytkownika o takim nicku')
    elif user.nick == user_to_map:
        map = folium.Map(
            location = get_coordinates_of(user.miasto),  
            titles='OpesStreetMap', 
            zoom_start=10)
        folium.Marker(
            location= get_coordinates_of(user.miasto), 
            popup=f'{user.miasto} tu mieszka {user.nick} ma na imię {user.imię} i wysłał {user.posty} posty'
            ).add_to(map)
        map.save(f'mapapojedyncza.html') 
        print(f'Mapa użytkownika {user.nick} pomyślnie wygenerowana :)')
    
def pogoda_z(miasto:str):
    url = f'https://danepubliczne.imgw.pl/api/data/synop/station/{miasto}'
    return requests.get(url).json()
    
