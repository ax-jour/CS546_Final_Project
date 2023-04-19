import sqlite3
from flask import Flask, render_template, jsonify, request, make_response, url_for, redirect
from flask_cors import CORS, cross_origin
import json

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def init_db():
    conn = sqlite3.connect('database.db')
    with open('./sql_scripts/users.sql') as f:
        conn.executescript(f.read())
    with open('./sql_scripts/votes.sql') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def row_to_dict(row):
    if type(row) == sqlite3.Row:
        return dict(zip(row.keys(), row))
    elif type(row) == list:
        return [dict(zip(r.keys(), r)) for r in row]
    else:
        return None

# TODO: Implement Zero Knowledge Proof Setup Step
def setup(circuit, lambda_v):
    prover_key = (0, 0)
    verifier_key = (0, 0)

    return prover_key, verifier_key

# TODO: Implement Zero Knowledge Proof Proving Step
def proving(user_id, proof, hashed_secret):
    return False

# TODO: Check vote is completed or not
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

init_db()



# Home Page
@app.route("/")
def index_page():
    conn = get_db_connection()
    votes = conn.execute('SELECT * FROM votes').fetchall()
    conn.close()
    return render_template('index.html', votes=votes)

# Trust Third Party
@app.route("/third_party")
def third_party_page():
    conn = get_db_connection()
    votes = conn.execute('SELECT * FROM votes').fetchall()
    conn.close()
    return render_template('trust_third_party.html', votes=votes)


# Signup Page
@app.route("/signup_page")
def signup_page():
    return render_template('signup.html')


# Login Page
@app.route("/login_page")
def login_page():
    return render_template('login.html')


# Vote Page
@app.route("/vote_page/<vote_id>", methods=['GET'])
def vote_page(vote_id):
    conn = get_db_connection()
    vote = conn.execute('SELECT * FROM votes WHERE vote_id = ?', (vote_id)).fetchone()
    conn.close()
    return render_template('voting.html', vote=vote)


# Vote Result Page
@app.route("/vote_result/<vote_id>", methods=['GET'])
def vote_result_page(vote_id):
    conn = get_db_connection()
    vote = conn.execute('SELECT * FROM votes WHERE vote_id = ?', (vote_id)).fetchone()
    conn.close()
    return render_template('results.html', vote=vote)


# Signup Request API endpoint
# Input: user_id, invitation_code
# Output: prover_key, verifier_key
@app.route("/signup", methods=['GET', 'POST'])
@cross_origin()
def signup():
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        user_id = data['user_id']
        invite_code = data['invitation_code']

        if invite_code != 111222:
            return 'Invalid Invitation Code'

        lambda_v, circuit = 0, 0
        pk, vk = setup(circuit, lambda_v)

        pk_string = str(pk[0]) + ',' + str(pk[1]) 
        vk_string = str(vk[0]) + ',' + str(vk[1])

        conn = get_db_connection()
        conn.execute('INSERT INTO users (user_id, prover_key, verifier_key) VALUES (?, ?, ?)',(user_id, pk_string, vk_string))
        conn.commit()
        conn.close()
        return vk_string
    else:
        return 'Error'
    

# Login Request API endpoint
# Input: user_id
# Output: prover_key
@app.route("/login", methods=['GET', 'POST'])
@cross_origin()
def login():
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        user_id = data['user_id']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE user_id = ?', user_id).fetchone()
        conn.close()
        if user is None:
            return 'Invalid User ID'
        else:
            return user['prover_key']
    else:
        return 'Error'
    

# Voting Request API endpoint
# Input: vote_id, user_id, proof(Pf), vote, hashed_secret(H)
# Output: Success or Error
@app.route("/vote", methods=['GET', 'POST'])
@cross_origin()
def vote():
    if request.method == 'POST':
        data = request.get_json()
        vote_id = data['vote_id']
        user_id = data['user_id']
        Pf = data['proof']
        hashed_secret = data['hashed_secret']
        vote_selection = data['vote_choice']

        conn = get_db_connection()
        verifier_key = conn.execute('SELECT verifier_key FROM users WHERE user_id = ?', (user_id,)).fetchone()
        conn.close()

        # TODO: Step 1: Verify proof
        if proving(verifier_key, Pf, hashed_secret):
            response = make_response('Rejected', 400)
            return response
        
        # TODO: Step 2: Check vote is completed or not
        if isVoteCompleted(vote_id):
            response = make_response({'message':'Vote closed'}, 400)
            return response

        # TODO: Step 2: Check duplicate vote in blockchain
        if isDuplicateVote(user_id, vote_id):
            response = make_response('Vote duplicated', 400)
            return response

        # TODO: Step 3: Update vote into blockchain

        # TODO: Step 4: Update vote counter in database
        conn = get_db_connection()
        vote = conn.execute('SELECT * FROM votes WHERE vote_id = ?', (vote_id,)).fetchone()
        vote_dict = row_to_dict(vote)

        vote_ct = vote_dict[vote_selection+"_ct"] + 1

        conn.execute('UPDATE votes SET ' + vote_selection + '_ct' + ' = ? WHERE vote_id = ?', (vote_ct, vote_id))
        conn.commit()        
        conn.close()

        response = make_response({'message':'Success'}, 200)
        return response
    else:
        response = make_response({'message':'Error'}, 400)
        return response