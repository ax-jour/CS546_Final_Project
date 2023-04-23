from blockchain import *

# Check duplicate vote in blockchain
def isDuplicateVote(blockchain, pk, hs):
    block_index = 1

    while block_index < len(blockchain.chain):
      block = blockchain.chain[block_index]
      trip = block['data']
      data = trip[0]
      
      if data['prover key'] == pk & data['hashed secret'] == hs:
          return True
      else:
          continue

    block_index += 1
    
    return False
