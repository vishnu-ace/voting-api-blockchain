from flask import Flask, redirect, url_for, request, jsonify
from dummy import BlockChain
from collections import Counter
import re
import sqlite3

app = Flask(__name__)

#Helper Function

#Function to check for data

def getApp():
    return app

def printSubsInDelimeters(str):
 
    
    regex = "\\{(.*?)\\}"
 
    
    matches = re.findall(regex, str)
 
    return matches[0]

@app.route('/')
def home():
    result = {'name':'Bisnu Nath'}
    return jsonify(result)

@app.route('/post/', methods = ['POST'])
def addData():
    blockchain = BlockChain()
    last_block = blockchain.latest_block
    last_proof_no = last_block.proof_no
    proof_no = blockchain.proof_of_work(last_proof_no)

    blockchain.new_data(
        
        recipient=request.json['name']
    )

    last_hash = last_block.calculate_hash
    block = blockchain.construct_block(proof_no, last_hash)

    #Adding data into DB

    conn = sqlite3.connect('voterDB.db')
    cur = conn.cursor()

    temp1 = printSubsInDelimeters(str(blockchain.chain[-1]))
    ss1 = temp1[14:20]
    ss2 = ''.join(ss1)
    

    cur.execute(
        'INSERT INTO candidate VALUES (?)', [ss2]
    )
    conn.commit()
    conn.close()

    return 'Successful'

@app.route('/blockchain/')
def getBlock():

    conn = sqlite3.connect('voterDB.db')

    cur  = conn.cursor()

    cur.execute(
        'SELECT * FROM candidate'
    )

    res = cur.fetchall()
    templist = [''.join(i) for i in res]
    print(templist)

    returnObject = Counter(templist)
    result = []
    for key,value in returnObject.items():
        temp = {'name' : key, 'value' : value}
        result.append(temp)

    
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
