from database import *

baza = 'server_db.db'

def wszystkie_wiadomosci():
    print('All messages:')

    stored_messages = all_messages(create_connection(baza))

    for stored_message in stored_messages:
        print(stored_message[0] + ': ' + stored_message[1])

    print('==KONIEC HISTORI==')
    print('')

def wyczysc():
    print('Delete messages:')

    check=input('Jesteś pewny? y -> tak: ')

    if check=='y':
        clear_chat(create_connection(baza))
        print('Usunieto')
    else:
        print('Nie usunieto')
    print('')

def uzytkownicy():
    print('Users:')

    users = all_users(create_connection(baza))

    for user in users:
        print(f'{user[0]}: {user[1]}')

    print('')

def dodaj_uzutkownika():
    login = input('Podaj nick do dodania: ')

    check = check_exist_user(create_connection(baza), (login,))
    print(check)
    if check:
        print(f'Uzytkownik {login} już istnieje')
        print('')
    else:
        add_user(create_connection(baza), (login,))

        print(f'Dodano nowego uzytkownika {login}')
        print('')

def usun_uzytkownika():
    login = input('Kogo usunąć: ')

    check = check_exist_user(create_connection(baza), (login,))
    if check:
        remove_user(create_connection(baza), (login,))
        print(f'Usunieto uzytkownika {login}')
        print('')
    else:
        print(f'Nie znaleziono uzytkownika {check}')
        print('')

def testowa_wiadomosc():
    login='DEBUG'

    check = check_exist_user(create_connection(baza), (login,))

    if not check:
        add_user(create_connection(baza), (login,))

    message='TESTOWA WIADOMOŚĆ (dibag.py)'

    login_id=check_exist_user(create_connection(baza), (login,))
    result=insert_message(create_connection(baza),login_id,message)

    if result:
        print('Dodano testową wiadomość!')
    else:
        print('Błąd dodawania wiadomości')

    print('')

def dodaj_user_z_id():
    login = input('Podaj nick do dodania: ')

    check = check_exist_user(create_connection(baza), (login,))
    # print(check)

    if check:
        print(f'Uzytkownik {login} już istnieje')
        print('')
        return 0

    id_check=int(input('Podaj ID: '))

    id_valid=check_users_id(create_connection(baza),(id_check,))
    # print(nowy)
    if id_valid:
        print(f'Wybrane ID:{id_check} jest zajęte !')
        print('')
        return 0

    add_user_with_id(create_connection(baza), id_check, login)

    print(f'Dodano nowego uzytkownika {login}')
    print('')

if __name__ == '__main__':
    print('Choose:')
    while True:
        print('1->All messages \n'
              '2->Clear chat\n'
              '3->Show users\n'
              '4->Add user\n'
              '5->Remove user\n'
              '6->Send test message\n'
              '7->Add user with ID\n'
              '0->Exit')
        choice = int(input('->:') or 22)

        if choice == 1:
            wszystkie_wiadomosci()

        elif choice == 2:
            wyczysc()

        elif choice == 3:
            uzytkownicy()

        elif choice == 4:
            dodaj_uzutkownika()

        elif choice == 5:
            usun_uzytkownika()

        elif choice==6:
            testowa_wiadomosc()

        elif choice==7:
            dodaj_user_z_id()

        elif choice == 0:
            print('Bye')
            break

        else:
            print('Nie obsługuje tej opcji :(')
            print('')
