from dane import users_list
def menu():
    while True:
        print('Witaj')
        #Dodaj
        print('Naciśnij [1] aby dodać użytkownika' )
        #Wyswietl
        print('Naciśnij [2] aby wyświetlić użytkownika' )
        #Zmien
        print('Naciśnij [3] aby zmienić dane użytkownika' )
        #Usun
        print('Naciśnij [4] aby usunąć użytkownika' )
        #Zakończ
        print('Naciśnij [0] aby zakończyć program' )

        choice = input('Wybierz funkcję do wykonania ')
        match choice :
            case '1':    
                add_user_to(users_list)
            case '2':   
                show_users_list(users_list)
            case '3':
                update_user(users_list)
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
        
def update_user(user_data: list[str,str,int]) -> None:
    nick_of_user = input("Podaj nick użytkownika do modyfikacji: ")
    print(nick_of_user)

    for user in users_list:
        if user['nick'] == nick_of_user:
            print("Znaleziono")
            # user['name'] = input("Podaj nowe imię: ")
            # user['nick'] = input("Podaj nową ksywe: ")
            # user['posts'] = int(input("Podaj nową liczbę postów: "))
            new_name = input("Podaj nowe imię: ")
            if new_name.__len__() > 0:
                user['name'] = new_name
            new_nick = input("Podaj nową ksywe: ")
            if new_nick.__len__() > 0:
                user['nick'] = new_nick
            new_posts = input("Podaj nową liczbę postów: ")
            if new_posts.isnumeric():
                user['posts'] = int(new_posts)
            return