import datetime
import hashlib
import json, database


class Blockchain(object):
  #create the first block and set its hash to '0'
  def __init__(self):
    self.data = []
    self.chain = []
    self.create_block(previous_hash='First block', proof=1)
  

  #add another block to the chain
  def create_block(self, proof, previous_hash=None):
    block = {'index': len(self.chain)+1,
             'timestamp': str(datetime.datetime.now()),
             'proof': proof,
             'previous_hash': previous_hash or self.hash(self.chain[-1]),
             'data': self.data
             }
    
    print('self.data', self.data)
    trip = block['data']
    print(len(trip))
    data = trip[0]
    data0 = data['prover key']
    data1 = data['hashed secret']
    data2 = data['vote']
    # print()
    # print("empty?", block['data'])
    # data0 = block['data']['prover key']
    # data1 = block['data']['hashed secret']
    # data2 = block['data']['vote']
    conn = database.get_db_connection()
    conn.execute("INSERT INTO blockchain (idx, ts, proof, previous_hash, data_pk, data_hs, data_vote) VALUES (?, ?, ?, ?, ?, ?, ?)", \
                 (block['index'], block['timestamp'], block['proof'], block['previous_hash'], data0, data1, data2))
    conn.commit()
    conn.close()

    self.data = []


    # conn = database.get_db_connection()
    # blockchain_list = conn.execute("SELECT * FROM blockchain")
    # conn.commit()
    # conn.close()

    # bc_ls = database.row_to_dict(blockchain_list)
    # # [{}, {}, {}]

    # for bc in bc_ls:
    #     index = bc['idx']
    #     ts = bc['ts']
    #     proof = int(bc['proof'])
    

    self.chain.append(block)
    return block
  

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
      else:
        b += 1

      block_index +=1

    return (a,b)




#blockchain = Blockchain()

#blockchain.mineblock(7,7,True)
#blockchain.mineblock(3,2,False)

#blockchain.printchain()

#print(blockchain.chain_valid())

#print(blockchain.countvotes())


