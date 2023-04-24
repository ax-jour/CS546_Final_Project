import datetime
import hashlib
import json, database


class Blockchain(object):
  #create the first block and set its hash to '0'
  def __init__(self):
    self.data = []
    self.chain = []
    self.create_blockfirst(previous_hash='1', proof=1)
  

  def create_blockfirst(self, proof, previous_hash=None):
    block = {'index': len(self.chain)+1,
             'timestamp': str(datetime.datetime.now()),
             'proof': proof,
             'previous_hash': previous_hash or self.hash(self.chain[-1]),
             'data': [0, 0, "Head: Ignore"]
             }
    
    data0 = 0
    data1 = 0
    data2 = "Head: Ignore"

    conn = database.get_db_connection()
    result = conn.execute("SELECT * FROM blockchain").fetchall()
    bc_ls = database.row_to_dict(result)

    
    if(bc_ls == []):
      conn.execute("INSERT INTO blockchain (idx, ts, proof, previous_hash, data_pk, data_hs, data_vote) VALUES (?, ?, ?, ?, ?, ?, ?)", \
                 (block['index'], block['timestamp'], block['proof'], block['previous_hash'], data0, data1, data2))
    conn.commit()
    conn.close()

    self.data = []    

    self.chain.append(block)
    return block

  #add another block to the chain and store in database
  def create_block(self, proof, previous_hash=None):
    block = {'index': len(self.chain)+1,
             'timestamp': str(datetime.datetime.now()),
             'proof': proof,
             'previous_hash': previous_hash or self.hash(self.chain[-1]),
             'data': self.data
             }
    
    trip = block['data']
    dat = trip[0]
    data0 = str(dat['prover key'])
    data1 = str(dat['hashed secret'])
    data2 = str(dat['vote'])
    conn = database.get_db_connection()
    conn.execute("INSERT INTO blockchain (idx, ts, proof, previous_hash, data_pk, data_hs, data_vote) VALUES (?, ?, ?, ?, ?, ?, ?)", \
                 (block['index'], block['timestamp'], block['proof'], block['previous_hash'], data0, data1, data2))
    conn.commit()
    conn.close()

    self.data = []    

    self.chain.append(block)
    return block
  

  #add block back into chain from database when restarting
  def restart_chain(self):
     conn = database.get_db_connection()
     blockchain_list = conn.execute("SELECT * FROM blockchain").fetchall()
     bc_ls = database.row_to_dict(blockchain_list)
     # [{}, {}, {}]
     conn.commit()
     conn.close()

     list = []

     if (not bc_ls == []):
      for bc in bc_ls:
          indx = bc['idx']
          ts = bc['ts']
          prf = int(bc['proof'])
          p_h = str(bc['previous_hash'])
          self.setdata(int(bc['data_pk']), int(bc['data_hs']), str(bc['data_vote']))

          block = {'index': indx,
              'timestamp': ts,
              'proof': prf,
              'previous_hash': p_h,
              'data': self.data
              }
         
          self.data=[]
          list.append(block)
     
     if (not list == []):
      self.chain = list 
     print ("Blockchain restored")


  #display previous block
  def print_previous_block(self):
    return self.chain[-1]
  

  #cryptographic algorithm- must solve a difficult problem in order to generate a new block
  #calculates new proof based on old proof to demonstrate that this is the legitimate next block in the chain
  def proof_of_work(self, previous_proof):
    new_proof = 1
    check_proof = False

    while check_proof is False:
      hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
      if hash_operation[:5] == '00000':
        check_proof = True
      else:
        new_proof += 1
    
    return new_proof


  #encode the block
  def hash(self, block):
    encoded_block = json.dumps(block, sort_keys=True).encode()
    return hashlib.sha256(encoded_block).hexdigest()


  #takes info and increments vote count accordingly
  def setdata(self, provkey, hsecret, vote):
    temp = {
      'prover key': provkey,
      'hashed secret': hsecret,
      'vote': vote
      }
    self.data.append(temp)



  #mines the block- generates proof
  def mineblock(self, provkey, hsecret, vote):
    self.setdata(provkey, hsecret, vote)

    previous_block = self.print_previous_block()
    previous_proof = previous_block['proof']
    proof = self.proof_of_work(previous_proof)
    previous_hash = self.hash(previous_block)

    self.create_block(proof, previous_hash)
    print("Block added!")


  #check that proofs all match
  def chain_valid(self):
    previous_block = self.chain[1]
    block_index = 2

    while block_index < len(self.chain):
      block = self.chain[block_index]
      if block['previous_hash'] != self.hash(previous_block):
        return False

      previous_proof = previous_block['proof']
      proof = block['proof']
      hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()

      if hash_operation[:5]!= '00000':
        return False
      previous_block = block
      block_index +=1

    return True


  #better printing format
  def printchain(self):
    for block in self.chain:
      print (block)
      print('\n')


  #count votes
  def countvotes(self):
    a = 0
    b = 0
    block_index = 1

    while block_index < len(self.chain):
      block = self.chain[block_index]
      trip = block['data']
      data = trip[0]
      
      if data['vote'] == "A":
        a +=1
      elif data['vote'] == "B":
        b += 1

      block_index +=1

    return (a,b)




#blockchain = Blockchain()

#blockchain.mineblock(7,7,True)
#blockchain.mineblock(3,2,False)

#blockchain.printchain()

#print(blockchain.chain_valid())

#print(blockchain.countvotes())


