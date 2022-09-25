#!/usr/bin/python
# -*- coding:utf-8 -*-
import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO request (file_path, file_id) VALUES (?, ?)",
            ('sample', 'sample')
            )

connection.commit()
connection.close()