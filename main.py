import random, json
from flask import Flask, render_template, request, make_response, url_for, redirect
from flask_cors import CORS, cross_origin
from database import *
from vote import *
import zkp_prover as pr
import zkp_verifier as ve

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
init_db() # Initializing Database


'''
Zero Knowledge Proof Setup Parameters
'''
N = 16238557847571361432079207259416643917456544702863121607771071554190210386009
g = 7777


'''
Webpage Renders
'''
# Signup/Login Page
@app.route("/")
def index():
    invitation_code = request.cookies.get('invitation_code')
    if invitation_code:
        return redirect(url_for('challenge_page'))
    
    return render_template('index.html')


# Trust Third Party
@app.route("/third_party_page")
def third_party_page():
    return render_template('trust_third_party.html')


# Challenge Page
@app.route("/challenge_page")
def challenge_page():
    invitation_code = request.cookies.get('invitation_code')
    if invitation_code is None:
        return redirect(url_for('index'))
    
    return render_template('challenge.html')


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



'''
POST API endpoints
'''
# Signup Request API endpoint
# Input: user infos, invitation_code
# Output: null
@app.route("/signup", methods=['POST'])
@cross_origin()
def signup():
    data = request.get_json()
    invitation = data['invitation']

    conn = get_db_connection()
    invitation_code = conn.execute('SELECT invitation_code FROM users_thirdparty WHERE invitation_code = ?', (invitation,)).fetchone()
    conn.commit()

    if invitation_code is None:
        conn.close()
        return make_response({'message':'Need authorized first.'}, 400)
    
    conn.execute('INSERT INTO users (invitation_code) VALUES (?)', (invitation,))
    conn.commit()
    conn.close()

    # ****** Below part should work on client side in real world ******
    # Simulating y = g^x mod N was calculate by client and send to server
    fName = data['first_name']
    lName = data['last_name']
    x = pr.hashed_secret((fName+lName).encode('utf-8'), N)
    encrypted_y = pr.get_y(x, g, N)
    # ****** Above part should work on client side in real world ******

    # Update y to user table
    ve.save_y(invitation, encrypted_y)

    return make_response({'message':'Success'}, 200)
    

# Login Request API endpoint
# Client login with calcuated t = g^v mod N and invitaion_code
# Input: invitaion_code
# Output: redirect to challenge page
@app.route("/login", methods=['POST'])
@cross_origin()
def login():
    # ****** Below part should work on client side in real world ******
    # Simulating t = g^v mod N was calculate by client and send to server
    v = random.randint(1, N)
    t = pow(g, v, N)
    # ****** Above part should work on client side in real world ******

    data = request.get_json()
    invitation_code = data['invitation_code']

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE invitation_code = ?', (invitation_code,)).fetchone()
    conn.commit()
    conn.close()
    if user is None:
        return make_response({'message':'User not exist!'}, 400)
    
    c = ve.gen_c(N)

    response = make_response({'message':'Success'}, 200)
    response.set_cookie('invitation_code', json.dumps(invitation_code))
    response.set_cookie('saved_v', json.dumps(v))
    response.set_cookie('saved_c', json.dumps(c))
    response.set_cookie('saved_t', json.dumps(t))
    
    return response


# Logout Request API endpoint
# Input: null
# Output: redirect to login page
@app.route("/logout", methods=['POST'])
@cross_origin()
def logout():
    response = make_response({'message':'Success'}, 200)
    response.set_cookie('invitation_code', '', expires=0)
    response.set_cookie('saved_v', '', expires=0)
    response.set_cookie('saved_c', '', expires=0)
    response.set_cookie('saved_t', '', expires=0)
    
    return response

    

# Challenge Request API endpoint
# Input: random number c
# Output: selected t and calculated r
@app.route("/challenge", methods=['POST'])
@cross_origin()
def challenge():
    data = request.get_json()

    invitation_code = int(request.cookies.get('invitation_code').replace('"', ''))
    if invitation_code is None:
        return make_response({'message':'Please login first!'}, 400)

    c = int(request.cookies.get('saved_c'))
    v = int(request.cookies.get('saved_v'))
    t = int(request.cookies.get('saved_t'))

    # ****** Below part should work on client side in real world ******
    # Simulating r = v - c * x was calculate by client and send to server
    fName = data['first_name']
    lName = data['last_name']
    x = int(pr.hashed_secret((fName+lName).encode('utf-8'), N))
    r = v - c * x
    # ****** Above part should work on client side in real world ******

    conn = get_db_connection()
    y = conn.execute('SELECT saved_y FROM users WHERE invitation_code = ?', (invitation_code,)).fetchone()
    conn.commit()
    conn.close()
    if y is None:
        return make_response({'message':'Cannot find hashed_secret!'}, 400)
    
    y = int(row_to_dict(y)['saved_y'])

    if ve.verification(y, r, t, c, g, N):
        print('Verification Success')
        return make_response({'message':'Verification Success'}, 200)
    else:
        print('Verification Fail')
        return make_response({'message':'Verification Fail'}, 400)
    

# Voting Request API endpoint
# Input: vote_id, user_id, proof(Pf), vote, hashed_secret(H)
# Output: Success or Error
@app.route("/vote", methods=['POST'])
@cross_origin()
def vote():
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
    

# Get third party's verification code
# Intput: user's first name, and last name
# Output: invite code
@app.route("/get_invitation_code", methods=['POST'])
@cross_origin()
def get_invitation_code():
    data = request.get_json()
    first_name = data['first_name']
    last_name = data['last_name']
    driver_license = data['driver_license']

    invitation_code = random.randint(0, 999999)
    conn = get_db_connection()
    conn.execute('INSERT INTO users_thirdparty (invitation_code, fName, lName, dLicense) VALUES (?,?,?,?)',(invitation_code,first_name,last_name,driver_license))
    conn.commit()        
    conn.close()
    
    response = make_response({'message':str(invitation_code)}, 200)
    return response