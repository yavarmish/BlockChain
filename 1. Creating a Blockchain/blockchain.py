from datetime import datetime
import hashlib
import json 
from flask import Flask,jsonify

# Building a blockchain

# Constructor: Initializes the blockchain with an empty chain and creates genesys block
# CreateBlock(POW,prevHash):  Creates a block, requires proof of work/stake and previous hash
# proofOfWork(prevProof): returns the newProof of work when some initial prevProof is given
# hash(block): creates the hash for a block
# isChainValid(chain): Returns if chain is valid by hashing data in previous block and checking
#                 if hash matches with previous hash field of the current block and confirming that 
#                 hash operation of the previous block and current block leads to a hash within the target range

class Blockchain:
    def __init__(self):
        self.chain = []
        self.createBlock(1,'0')
    def createBlock(self,proofOfWork, prevHash):
            block = {            
                "timestamp" : str(datetime.now()),
                "prevHash" : prevHash,
                "proof" : proofOfWork,
                "index" : len(self.chain)+1
            }
            self.chain.append(block)
            return block
    def proofOfWork(self,currentNonce):
        newNonce = 1
        checkProof = False
        while checkProof is False:
            myHash  = hashlib.sha256(str(currentNonce**2 - newNonce**2).encode()).hexdigest();
            if myHash[:4] == '0000':
                checkProof = True
            else:
                newNonce+=1
        return newNonce
# Utility function, can ignore
    def serialize_datetime(obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        raise TypeError("Type not serializable")
  
    def hash(self,block):
        encoded_block = json.dumps(block,sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    def isChainValid(self,chain):
        prevBlock = chain[0]
        i = 1
        while i < len(chain):
            block = chain[i]
            if block["prevHash"] != self.hash(prevBlock):
                return False
            prevProof = prevBlock["proof"]
            proof = block["proof"]
            myHash  = hashlib.sha256(str(prevProof**2 - proof**2).encode()).hexdigest()
            if(myHash[:4] != '0000'):
                return False
            prevBlock = block
            i+=1
        return True
    
# Mining The BLockchain
app = Flask(__name__)
blockchain = Blockchain()
@app.route('/mineBlock/',methods=['GET'])
def mineBlock():
    lastBlock = blockchain.chain[-1];
    lastProof = lastBlock['proof']
    proof = blockchain.proofOfWork(lastProof)
    prevHash = blockchain.hash(lastBlock)
    newBlock = blockchain.createBlock(proof, prevHash)
    response = {'message': 'Congrats! you just mined a block',
                'index': newBlock['index'],
                'timestamp':newBlock['timestamp'],
                'proof':newBlock['proof'],
                'prevHash': newBlock['prevHash']}
    return jsonify(response), 200

# Getting the blockchain
@app.route('/getChain',methods=['GET'])
def getChain():
    response = {'chain': blockchain.chain,
                'length':len(blockchain.chain)}
    return jsonify(response), 200

# Checking if Blockchain is Valid
@app.route('/isValid',methods=['GET'])
def isValid():
    isValid = blockchain.isChainValid(blockchain.chain)
    if isValid:
        response = "Valid"
    else:
        response = "Invalid"
    return jsonify(response), 200

#Running the app
app.run(host='0.0.0.0',port=5000)

