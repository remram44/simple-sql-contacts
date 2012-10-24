from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from contacts.menus import Menu, Option
from contacts import models


engine = create_engine('sqlite:///database.sqlite3', echo=True)

Session = sessionmaker(bind=engine)


def new_user():
    pass


def search_user():
    pass


menu = Menu([
        Option("Create a new user", callback=new_user),
        Option("Search a user by name", callback=search_user),
        Option("Exit", value='exit'),
    ])


def main():
    ret = None
    while ret != 'exit':
        ret = menu.select()
