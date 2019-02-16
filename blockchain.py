import random
import hashlib, json 
import requests
from urllib.parse import urlparse
from time import time
from block_data import Data

class Blockchain():
    
    def __init__(self):
        self.chain = []
        self.current_transactions= []
        self.nodes = set()
        #genesis block
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof , previous_hash=None):
        block ={
            'index': len(self.chain) + 1 ,
            'timestamp' : time(), 
            'transactions': self.current_transactions,
            'proof' : proof, 
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }
        self.current_transactions=[]
        self.chain.append(block)
        return block

    def new_transaction(self,*args, **kwargs):
        data = Data(*args, **kwargs)
        self.current_transactions.append(
            data.serialize()
        )
        return self.last_block['index']+1

    @staticmethod
    def hash(block):
        block_string = json.dumps(block , sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1] 
    def proof_of_work(self , last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof+=1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:5]== '00000'

    def register_node(self , address, flag):
        parsed_url = urlparse(address)
        if parsed_url.netloc != "":
            if flag == 1:
                self.trigger_flood_nodes(address)
                for node in self.nodes:
                    node = "http://" + node
                    requests.post(url=f'http://{parsed_url.netloc}/nodes/register', json={
                        'nodes': [node],
                        'flag': 0
                    })
            self.nodes.add(parsed_url.netloc)

    def valid_chain(self , chain):
        last_block = chain[0]
        for current_index in range(1 , len(chain)):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print('\n----------\n')
            if block['previous_hash']!=self.hash(last_block):
                return False
            if not self.valid_proof(last_block['proof'] , block['proof']):
                return False
            last_block = block
        else:
            return True

    def resolve_conflicts(self):
        neighbours = self.nodes
        new_chain = None
        max_length = len(self.chain)
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')
            if response.status_code ==200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length >= max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain
        if new_chain:
            self.chain = new_chain
            return True
        return False

    def triggered_flood_chain(self):
        for node in self.nodes:
            requests.get(f'http://{node}/nodes/resolve')

    def trigger_flood_nodes(self,address):
        for node in self.nodes:
            requests.post(url=f'http://{node}/nodes/register', json={
                'nodes': [address] ,
                'flag': 0
            })
