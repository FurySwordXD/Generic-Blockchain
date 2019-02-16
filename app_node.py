from blockchain import Blockchain
from block_data import Data

from flask import Flask, jsonify, request, render_template, redirect
from flask_cors import CORS
import json
import hashlib
from sys import argv

app = Flask(__name__)

CORS(app)
blockchain = Blockchain()

@app.route("/")
def index():
    return render_template("admin.html", data=Data().required())

@app.route('/mine', methods= ['GET'])
def mine():
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    with open("data/"+str(port)+"_chain.json", "w") as file:
        json.dump(blockchain.chain, file)

    response = {
        'message' : "New Block Forged",
        'index': block['index'] , 
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    blockchain.triggered_flood_chain()
    return jsonify(response) , 200


@app.route('/transactions', methods=['GET'])
def full_transactions():
    return jsonify({
        'transactions': blockchain.current_transactions
    })

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    print(values)
    required = Data().required()
    print(required)
    if not all(k in values for k in required):
        return 'missing values' , 400

    index = blockchain.new_transaction(**values)
    response = {'message': f'Transaction will be added to Block {index} '}
    return jsonify(response) , 201

@app.route('/chain', methods=['GET'])
def full_chain():
    response={
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route('/block/<private_key>', methods=['GET'])
def get_block(private_key):
    public_key = hashlib.sha256(private_key.encode()).hexdigest()
    blocks = []
    for block in blockchain.chain:
        for transaction in block['transactions']:
            if public_key == transaction['public_key']:
                blocks.append(transaction)           
    
    response = {
        'transactions': blocks,
        'length': len(blocks),
    }
    return jsonify(response), 200

@app.route('/nodes', methods=['GET'])
def full_nodes():
    return jsonify({
        'nodes': list(blockchain.nodes)
    })

@app.route('/nodes/register', methods= ['POST'])
def register_nodes():
    values = request.get_json()
    nodes = values.get('nodes')
    flag = values.get('flag')
    print(flag)
    if nodes is None:
        return 'Error: Please supply a valid list of nodes' , 400
    for node in nodes:
        blockchain.register_node(node, flag)
    response = {
        'message' : 'new nodes have been added', 
        'total_nodes': list(blockchain.nodes)
    }
    blockchain.resolve_conflicts()

    with open("data/"+str(port)+"_chain.json", "w") as file:
        json.dump(blockchain.chain, file)

    return jsonify(response) , 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        with open("data/"+str(port)+"_chain.json", "w") as file:
            json.dump(blockchain.chain, file)
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain,
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain,
        }
    return jsonify(response), 200
                    
if __name__ == "__main__":
    
    try:
        port = argv[1]
    except:
        port = 5001

    try:
        with open("data/"+str(port)+"_chain.json", "r") as file:
            blockchain.chain = json.loads(file.read())
    except:
        file = open("data/"+str(port)+"_chain.json", "w")
        file.close()
    app.run(host='0.0.0.0', port=port, debug=True)