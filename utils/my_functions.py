from dane import users_list
def menu():
    while True:
        print('Witaj')
        #Dodaj
        print('Naciśnij [1] aby dodać użytkownika' )
        #Wyswietl
        print('Naciśnij [2] aby dodać użytkownika' )
        #Zmien
        print('Naciśnij [3] aby dodać użytkownika' )
        #Usun
        print('Naciśnij [4] aby dodać użytkownika' )
        #Zakończ
        print('Naciśnij [0] aby zakończyć program' )

        choice = input('Wybierz funkcję do wykonania ')
        match choice :
            case '1':    
                add_user_to(users_list)
            case '2':   
                show_users_list(users_list)
            case '4':   
                del_user_to(users_list)
            case '0':  
                print('Do zobaczenia!') 
                return
            
        for user in users_list:
            print (f'twoj znajomy {user["nick"]} opublikował {user["posts"]} postów')

def show_users_list(users_list:list) -> None:
    for user in users_list:
        print(user)
    
def add_user_to(users_list:list) -> None: 
    """Add object to list
    
    Args:
        users_list (list): lista użytkowników
    """
    name = input('Podaj imię ')
    nick = input('Podaj nick ')
    posty = input('Podaj ilość postów ')
    users_list.append({"name":name,"nick":nick,"posts":posty})
    
def del_user_to(users_list:list) -> None:
    """Remove object from list

    Args:
        users_list (list): lista użytkowników
    """
    tmp_list = []
    name = input('Podaj imię użytkownika do znalezienia ')
    for user in users_list:
        if user ["name"] == name:
            tmp_list.append(user)
    for nr, users_to_remove in enumerate(tmp_list):
        print(f'Znaleziono użytkowników {nr+1} {users_to_remove} ')
    numer = int(input('Wybierz użytkownika do usunięcia '))
    if numer == 0:
        for user in tmp_list:
            users_list.remove(user)
    else:
        users_list.remove(tmp_list[numer-1])