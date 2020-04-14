from flask import Flask, jsonify, request
import json
import hashlib
import requests
import uuid
from time import time

#Blockchain class will contain a constructor that will initiate the chain and transaction list.
# The chain list will store our blockchain, whereas the transactions will be stored in the current_transacations array.
app = Flask(__name__)
node_identifier = str(uuid.uuid4()).replace('-',"")

class Blockchain:
    def __init__(self):
        self.current_transactions = []
        self.chain = []
        self.nodes = set()
        # Create the genesis block
        self.new_block(previous_hash='1', proof=100)

    # new_block function which will be used to create new blocks and then add them to the existing chain.
    def new_block(self,proof, previous_hash=None):
        block = {
            'index' : len(self.chain) + 1,
            'timestamp' : time(),
            'proof': proof,
            'transactions': self.current_transactions,
            'previous_hash' : previous_hash or self.hash(self.chain[-1]),
        }
        #set current transaction list to empty
        self.current_transactions = []
        self.chain.append(block)
        return block


    # The new_transaction method creates a new transaction and then add it to the already existing transaction list.
    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.last_block['index']+ 1

    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof,proof) is False:
            proof +=1

        return proof

    # Hash function is used for creating the hash for a block.
    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]


    # register_node() → To register a new node and add it to the network
    # valid_proof() → Will ensure wheather a submitted block to the chain solves the problem
    # valid_chain() → This will check if the subsequent blocks in the chain are valid or not.
    def register_node():
        pass

    def valid_chain():
        pass

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f"{last_proof}{proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"


blockchain = Blockchain()

@app.route('/mine',methods=['GET'])
def mine():
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block)
    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )
    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)
    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transactions():
    values = request.get_json()
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return "Missing values",400
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
    response = {'message': f"transaction is scheduled to be added to the block no. {index}"}
    return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain' : blockchain.chain,
        'length' : len(blockchain.chain)
    }
    return jsonify(response), 200

if __name__== '__main__':
    app.run()