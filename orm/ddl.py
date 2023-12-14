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