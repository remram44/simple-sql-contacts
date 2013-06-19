import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from contacts.menus import Menu, Option
from contacts import models


engine = create_engine('sqlite:///database.sqlite3', echo=True)

Session = sessionmaker(bind=engine)


def edit_user(person):
    pass


def new_user():
    print "Creating a new person"
    name = raw_input("  Name: ")
    if not name:
        print "Invalid name, aborting"
        return
    dob = raw_input("  Date of birth (YYYY/MM/DD): ")
    try:
        dob = datetime.datetime.strptime(dob, '%Y/%m/%d')
    except ValueError:
        dob = None
    if not dob:
        print "Invalid date, aborting"
        return

    session = Session()
    try:
        person = models.Person(name=name, dateofbirth=dob)
        session.add(person)
        session.commit()
    except Exception, e:
        session.rollback()
        print "Insertion failed (%s: %s)" % (e.__class__.__name__, e)
    else:
        print "Person created"
    finally:
        session.close()


def search_user():
    print "Searching for an existing person"
    name = raw_input("  Name pattern: ")
    if not name:
        print "Invalid name, aborting"

    session = Session()
    results = (
            session.query(models.Person)
                    .filter(models.Person.name.like(name))
                    .all())

    menu = Menu(
            [Option("%s" % p.name, value=i)
             for i, p in enumerate(results)] +
            [Option("Abort", value='exit')])
    choice = menu.select()
    if choice == 'exit':
        return
    edit_user(results[choice])


menu = Menu([
        Option("Create a new person", callback=new_user),
        Option("Search a person by name", callback=search_user),
        Option("Exit", value='exit'),
    ])


def main():
    if not engine.dialect.has_table(engine.connect(), 'person'):
        while True:
            a = raw_input("The tables don't seem to exist. Create them? "
                          "(y/n) ")
            if a == 'y':
                models.Base.metadata.create_all(bind=engine)
                break
            elif a == 'n':
                return

    ret = None
    while ret != 'exit':
        ret = menu.select()
