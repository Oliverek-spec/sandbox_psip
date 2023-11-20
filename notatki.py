from dane import users_list



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
            
            break
        
