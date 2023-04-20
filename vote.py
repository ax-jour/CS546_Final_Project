import sqlite3
from database import *

# Check vote is completed or not
def isVoteCompleted(vote_id):
    conn = get_db_connection()
    vote = conn.execute('SELECT * FROM votes WHERE vote_id = ?', (vote_id)).fetchone()
    vote_dict = row_to_dict(vote)

    if vote_dict['vote_isComplete']:
        conn.close()
        return True

    voted = vote_dict['op1_ct'] + vote_dict['op2_ct'] + 1
    if voted >= vote_dict['vote_participants_ct']:
        conn.execute('UPDATE votes SET vote_isComplete = TRUE WHERE vote_id = ?', (vote_id,))
        conn.commit()
        conn.close()
 
    return False

# TODO: Check duplicate vote in blockchain
def isDuplicateVote(user_id, vote_id):
    return False
