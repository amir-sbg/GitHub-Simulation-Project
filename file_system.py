import os
import pickle
import FileCodingHandler


class User:

    def __init__(self, username, password):
        self.__username = username
        self.__password = password
        self.__repositories = dict()

    def get_username(self):
        return self.__username

    def check_password(self, password):
        return self.__password == password

    def get_password(self):
        return self.__password

    def __eq__(self, other):
        return self.__username == other.get_username()

    def add_repository(self, repository_name):
        self.__repositories[repository_name] = set().add(self.__username)

    def get_repositories(self):
        return self.__repositories


def authenticate_user(username, password):
    users = load_users()

    for user in users:
        if user.get_username() == username and user.check_password(password):
            return user

    return None


def load_users():
    file = None
    try:
        file = open('./data/users.raw', 'rb')
        users = pickle.load(file)
    except IOError as er:
        users = list()
    finally:
        if file is not None:
            file.close()

    return users


def save_users(users):
    file = None
    try:
        file = open('./data/users.raw', 'wb')
        pickle.dump(users, file)
    except IOError as error:
        print(error)
    finally:
        file.close()


def allocate_new_user(username, password):
    users = load_users()

    new_user = User(username, password)

    for user in users:
        if new_user == user:
            return False

    users.append(new_user)

    save_users(users)

    base_directory = new_user.get_username()
    path = os.path.join('./data', base_directory)

    try:
        os.mkdir(path)
    except OSError as error:
        print(error)

    return True


def pull_server_side(username, password, path, type_):
    user = authenticate_user(username, password)
    if user is None:
        return None
    pathT = "data/" + user.get_username() + "/" + path
    return FileCodingHandler.encoder(type_, pathT)


def push_server_side(username, password, messageBody, path):
    user = authenticate_user(username, password)
    if user is None:
        return None
    pathT = "data/" + user.get_username() + "/" + path
    FileCodingHandler.decoder(messageBody, pathT)


def pull_client_side(path, type_):
    return FileCodingHandler.encoder(type_, path)


def push_client_side(messageBody, path):
    FileCodingHandler.decoder(messageBody, path)


def create_repository_for_user(username, password, repository_name):
    user = authenticate_user(username, password)
    users = load_users()
    if user is None:
        return False
    base_directory = user.get_username()
    path = os.path.join('./data', base_directory, repository_name)

    try:
        os.mkdir(path)
    except OSError as error:
        print(error)
    for user_ in users:
        if user_ == user:
            user_.add_repository(repository_name)
            break

    save_users(users)

    return True

