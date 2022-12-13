import csv
import sqlite3
import time
from sqlite3 import Error
from queue import Queue


def open_csvfile_athlete(file_pass):
    # with open(file_pass, 'r') as file:
    #     content = csv.DictReader(file)
    #     for row in content:
    #         print(row)
    content_q = Queue()
    # content = []
    with open(file_pass, 'r') as file:
        n = csv.DictReader(file)
        for row in n:
            name = row['Name'].replace('-','')
            sex = row['Sex']
            try:
                age = int(row['Age'])
            except Exception:
                age = 0
            try:
                height = int(row['Height'])
            except Exception:
                height = 0
            try:
                weight = int(row['Weight'])
            except Exception:
                weight = 0
            team = row['Team']
            noc = row['NOC']
            games = row['Games']
            try:
                year = int(row['Year'])
            except Exception:
                year = 0
            season = row['Season']
            city = row['City']
            sport = str(row['Sport']).replace("'", '').strip()
            event = str(row['Event']).replace("'", '').strip()
            medial = row['Medal']
            # content.append((
            #     name, sex, event
            # ))
            content_q.put_nowait((
                name, sex, age, height, weight, team, noc,
                games, year, season, city, sport, event, medial
            ))
        # print(content)
        vertex = content_q.get()
        print(vertex, content_q.qsize())
        return content_q


def open_csvfile_noc(file_pass):
    content = []
    with open(file_pass, 'r') as file:
        n = file.readlines()
        for i in range(1, len(n)):
            noc = n[i].strip().split(',')[0]
            country = n[i].strip().split(',')[1]
            notes = n[i].strip().split(',')[2]
            if not notes:
                notes = None
            # print(noc, country, notes)
            content.append((noc, country, notes))
        return content

def create_connection(dbpath):
    connection = None
    try:
        connection = sqlite3.connect(dbpath)
    except Error as error:
        print('Wrong connection', error)
    return connection


def get_queries(connection, queries):
    cursor = connection.cursor()
    try:
        cursor.execute(queries)
        connection.commit()
    except Error as error:
        print('Wrong execute', error)


def create_table_athletevents(data_name):
    connection = create_connection(data_name)
    athlet_events_table = """
        CREATE TABLE IF NOT EXISTS athletevents(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            sex TEXT,
            age INTEGER,
            height INTEGER,
            weight INTEGER,
            team TEXT,
            NOC TEXT,
            games TEXT,
            year INTEGER,
            season TEXT,
            city TEXT,
            sport TEXT,
            event TEXT,
            medal TEXT,
            FOREIGN KEY (NOC) REFERENCES nocregions (region)             
        ); 
    """
    get_queries(connection, athlet_events_table)

def fill_athletevents_table(database, file_pass):
    content = open_csvfile_athlete(file_pass)
    connection = create_connection(database)
    print(content, content.qsize())
    while content.qsize() > 0:
        el = content.get()
        # print(el)
        fill_athletevents_table = f"""
            INSERT INTO athletevents
                (name, sex, age, height, weight, team, NOC, games, year,
                season, city, sport, event, medal)
            VALUES
                ('{el[0]}', '{el[1]}', '{el[2]}', '{el[3]}', '{el[4]}',
                 '{el[5]}', '{el[6]}', '{el[7]}', '{el[8]}', '{el[9]}',
                 '{el[10]}', '{el[11]}', '{el[12]}', '{el[13]}');
        """
        get_queries(connection, fill_athletevents_table)


def fill_nocregion_table(database, file_pass):
    content = open_csvfile_noc(file_pass)
    connection = create_connection(database)
    print(content)
    for el in content:
        fill_nocregion_table = f"""
            INSERT INTO 
                nocregions(region, country, notes)
            VALUES 
                ('{el[0]}', '{el[1]}', '{el[2]}')
            """
        get_queries(connection, fill_nocregion_table)


def create_table_nocregions(data_name):
    connection = create_connection(data_name)
    noc_region_table = """
        CREATE TABLE IF NOT EXISTS nocregions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            region TEXT,
            country TEXT,
            notes TEXT
        );
    """
    get_queries(connection, noc_region_table)


def delete_table(database, tablename):
    connection = create_connection(database)
    del_table = f"""DROP TABLE {tablename}"""
    get_queries(connection, del_table)


def main():
    database_name = 'csvfilesdb.db'
    file_nocregion = r'D:\MyPythonFolder\MyPython\.venv\Dif_files\csv\noc_regions.csv'
    file_athletevents = r'D:\MyPythonFolder\MyPython\.venv\Dif_files\csv\athlete_events.csv'
    # open_csvfile_athlete(file_athletevents)
    # open_csvfile_noc(file_nocregion)

    create_connection(database_name)
    create_table_nocregions(database_name)
    create_table_athletevents(database_name)

    fill_athletevents_table(database_name, file_athletevents)
    fill_nocregion_table(database_name, file_nocregion)

    # delete_table(database_name, 'athletevents')

if __name__ == '__main__':
    main()

