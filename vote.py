from blockchain import *

# Check duplicate vote in blockchain
def isDuplicateVote(blockchain, pk, hs):
    block_index = 0

    while (block_index < len(blockchain.chain)):
      block = blockchain.chain[block_index]
      trip = block['data']
      data = trip[0]
      
      if (int(data['prover key']) == pk and int(data['hashed secret']) == hs):
          return True
      else:
          block_index +=1
          continue
    
    return False
