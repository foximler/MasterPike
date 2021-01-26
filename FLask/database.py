# File to create a database and create a table if it doesn't already exist
import sqlite3
import time

def create_database():
    # Creates DB if it doesn't exist
    conn = sqlite3.connect('masterfish.db')
    cursor = conn.cursor()

    # Creates table if it doesn't exist
    query = """
    CREATE TABLE IF NOT EXISTS users (
        uuid STRING PRIMARY KEY,
        temp INTEGER,
        humid INTEGER,
        alert INTEGER,
        lat STRING,
        long STRING,
        time STRING,
        email STRING
    );
    """

    cursor.execute(query)
    cursor.close()

    return


def update_database(data):
    conn = sqlite3.connect('masterfish.db')
    cursor = conn.cursor()
    time_status = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(data['time'])))
    data["time"]=time_status

    # Need to use some sort of UPSERT to keep the email from being updated
    query1 = """
    INSERT OR IGNORE INTO users(uuid, temp, humid, alert, lat, long, time)
    VALUES(?, ?, ?, ?, ?, ?, ?)
    """

    query2 = """
    UPDATE users SET uuid=?, temp=?, humid=?, alert=?, lat=?, long=?, time=?
    """

    values = (data["uuid"], data["temp"], data["humid"], data["alert"], data["lat"], data["long"], data["time"])

    cursor.execute(query1, values)
    cursor.execute(query2, values)
    conn.commit()
    cursor.close()
    return

def getstatus(email):
    conn = sqlite3.connect('masterfish.db')
    c = conn.cursor()
    print(email)
    c.execute("SELECT * from users WHERE email=?",
    (email,))
    items = c.fetchall()
    conn.commit()
    c.close()
    return items