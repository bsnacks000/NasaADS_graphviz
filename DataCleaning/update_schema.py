# when new subject is added import the <subject>ORM module
from orm.starsORM import *
from orm.cosmologyORM import *
# <---- add new imports here before updating

def update_schema(db_path=None):
    if db_path != None:
        engine = create_engine('sqlite:///'+ db_path)  # <--- in real app this will be sqlite:///./App/db/graph.db
        Base.metadata.create_all(engine)
    else:
        print 'error: db_path not specified'

if __name__ == '__main__':
    update_schema(db_path='test.db')    # if script is called from shell builds a test in cwd
