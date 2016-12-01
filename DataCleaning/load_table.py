from odo import odo, discover, resource
from sqlalchemy import select, Table

# use odo to load from csv directly to sqlite3
# best to use this manually from a python script maybe with a loop.
# import sqlalchemy and pass in a conn,meta from outer scope to run check

def load_table(csv_file_name, db_path, conn, meta):

    table_name = csv_file_name.replace('.csv',"")

    # need to figure out way to connect and
    t = Table(table_name, meta, autoload=True)
    if len([row for row in conn.execute(select([t]))]) == 0:

        dshape =  discover(resource('./data/'+csv_file_name))
        odo('./data/'+csv_file_name, 'sqlite:///'+db_path+'::'+table_name,dshape=dshape)

    else:
        print "table:: "+table_name+' already contains records: no csv loaded '
