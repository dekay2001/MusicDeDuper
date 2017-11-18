import os
import sqlite3


class musicDeduperDBManager(object):
    def __init__(self):
        self.db_path = os.path.dirname(__file__)
        self.sqlite_file = os.path.join(self.db_path, 'mdd.sqlite')

    def initialize_new_db(self, sqlite_full_path):
        """Helper function to initialize the db.
        Caller should make sure it doesn't already exist."""
        if os.path.exists(sqlite_full_path):
            raise Exception('The database was already initialized.')
        conn = sqlite3.connect(sqlite_full_path)
        c = conn.cursor()
        result = c.execute('create table song_library(_id integer primary key autoincrement,\n '\
            +'keep integer default 1,\n'
            +'full_file_path text);')
        c.close()

    def initialize(self, full_db_file_path=None):
        """This is the function that will be called when
        the application is run for the first time that 
        will check and initialize everything it needs to
        to run the application db."""
        if full_db_file_path is None:
            full_db_file_path = self.sqlite_file
        if not os.path.exists(full_db_file_path):
            print('Initializing {}'.format(full_db_file_path))
            self.initialize_new_db(full_db_file_path)
        else:
            print('{} exists.'.format(full_db_file_path))


