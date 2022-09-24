import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO request (file_path, file_id) VALUES (?, ?)",
            ('/Users/cosmos/Desktop/Internship/INDIC OCR API/DocTR_Indic_OCR_API/src/uploads/img_2525bf49-888c-4fbb-88ea-63ad70d143ac.png', '32c6411c-973b-484a-a1c5-9c41d2213964')
            )

connection.commit()
connection.close()