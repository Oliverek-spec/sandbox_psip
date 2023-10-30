from dane import users_list

for user in users_list:
    print (f'twoj znajomy {user["nick"]} opublikował {user["posts"]} postów')
