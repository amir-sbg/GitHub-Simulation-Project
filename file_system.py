import os
import pickle


class User:

    def __init__(self, username, password):
        self.__username = username
        self.__password = password

    def get_username(self):
        return self.__username

    def check_password(self, password):
        return self.__password == password

    def __eq__(self, other):
        return self.__username == other.get_username()


def authenticate_user(username, password):
    users = load_users()
    user = None
    for u in users:
        if u.get_username() == username and u.check_password(password):
            user = u
            break

    return user


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


def pull_from_user_directory(username, password, directory_name, path, file_name=None, all_files=True):

    user = authenticate_user(username, password)
    if user is None:
        return None
    base_directory = user.get_username()
    path = os.path.join('./data', base_directory, path, directory_name)

    try:
        files = list()
        if all_files:
            for name in os.listdir(path):
                if os.path.isfile(os.path.join(path, name)):
                    with open(os.path.join(path, name), 'rb') as f:
                        files.append(f.read(-1))

        else:
            with open(os.path.join(path, file_name), 'rb') as f:
                files.append(f.read(-1))

        return files

    except OSError as error:
        print(error)
        return None


def create_directory_for_user(username, password, directory_name, path=''):

    user = authenticate_user(username, password)
    if user is None:
        return False
    base_directory = user.get_username()
    path = os.path.join('./data', base_directory, path, directory_name)

    try:
        os.mkdir(path)
    except OSError as error:
        print(error)

    return True


if __name__ == '__main__':
    print(allocate_new_user('Amir2w44', '00sdfasdf'))
    create_directory_for_user('Amir2w44', '00sdfasdf', 'HI')
    create_directory_for_user('Amir2w44', '00sdfasdf', 'H', 'HI')
    print(pull_from_user_directory('Amir2w44', '00sdfasdf', 'H', 'HI', all_files=True))
