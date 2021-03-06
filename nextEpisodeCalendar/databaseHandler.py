import sqlite3
import os.path

class DB:
    __TABLE = 'series'
    __NAME_COLUMN = 'name'
    __URL_COLUMN = 'url'

    def __init__(self, dbPath: str):
        self.dbPath = dbPath
        if (not os.path.exists(self.dbPath)):
            conn = sqlite3.connect(self.dbPath)
            c = conn.cursor()
            c.execute(f'''CREATE TABLE {DB.__TABLE} (
                            {DB.__URL_COLUMN} TEXT PRIMARY KEY,
                            {DB.__NAME_COLUMN} TEXT
                        )''')
            conn.commit()
            conn.close()
        self.conn = None
        self.cursor = None

    def __connect(self):
        self.conn = sqlite3.connect(self.dbPath)
        self.cursor = self.conn.cursor()

    def __close(self):
        self.conn.close()
        self.conn = None
        self.cursor = None

    def insert(self, name: str, url: str):
        self.__connect()

        try:
            self.cursor.execute(f'''INSERT INTO
                {DB.__TABLE} 
                ({DB.__NAME_COLUMN}, {DB.__URL_COLUMN}) 
                VALUES (?, ?)''', (name, url))
        except sqlite3.IntegrityError:
            print('Series already added')

        self.conn.commit()
        self.__close()

    def getAll(self):
        self.__connect()

        self.cursor.execute(f'''SELECT {DB.__NAME_COLUMN}, {DB.__URL_COLUMN} from {DB.__TABLE}''')

        res = self.cursor.fetchall()

        self.__close()
        
        return res
