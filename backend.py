import pandas as pd
import datetime

from pony.orm import *

db = Database()

class Person(db.Entity):
    name = Required(str)
    answer1 = Optional(str)
    answer2 = Optional(str)
    answer3 = Optional(str)

db.bind(provider='mysql', host='127.0.0.1', user='root', passwd='0000', db='training')
db.generate_mapping(create_tables=True)

@db_session
def create_user(name):
    p = Person.get(name=name)
    if p is None:
        #Person(name=name, answer1 = None, answer2 = None, answer3 = None)
        Person(name=name)

@db_session
def add_answer(name, answer_n, answer):
    id = Person.get(name=name).id
    if answer_n == 1:
        Person[id].answer1 = answer
    elif answer_n == 2:
        Person[id].answer2 = answer
    else:
        Person[id].answer3 = answer
