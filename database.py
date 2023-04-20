import sqlite3

def row_to_dict(row):
    if type(row) == sqlite3.Row:
        return dict(zip(row.keys(), row))
    elif type(row) == list:
        return [dict(zip(r.keys(), r)) for r in row]
    else:
        return None

def init_db():
    conn = sqlite3.connect('database.db')

    with open('./sql_scripts/users.sql') as f:
        conn.executescript(f.read())
    with open('./sql_scripts/thirdpartyusers.sql') as f:
        conn.executescript(f.read())
    with open('./sql_scripts/votes.sql') as f:
        conn.executescript(f.read())

    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_votes(vote_id):
    conn = get_db_connection()
    vote = conn.execute('SELECT * FROM votes WHERE vote_id = ?', (vote_id,)).fetchone()
    conn.close()
    return row_to_dict(vote)