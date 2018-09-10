# Notary Smart Contract Demo
# (c) Veriteos, Inc. 2018 
#
# Purpose
# Notarizes/Checks Notarization for a file of reading using a deployed smart contract.
# Demonstrates interacting with a smart contract on the permissioned Veriteos blockchain 
#
# Dependencies:
#    verify.sol
#    Note: Deploy contract first using deploycontract script or other method
#    This demo requires the deployed contract's address
#
# Sample File
#    Use demo file: elemental.csv
# 
# Contract Methods:
# Notarize: Stores the SHA256 for a given line of text.
# Validate: Check to see if a given piece of text was previously hashed (ie; has this line changed from when it was last seen)
#
# Usage: python NotarizeDemo.py -c verify.sol -a <contract address> [-p <provider endpoint>]

import sys
import web3
import argparse

from web3 import Web3
from solc import compile_source

# get command line arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--contract", required=True,
	help="filename of smart contract")
ap.add_argument("-a", "--address", required=True,
	help="Blockchain address of deployed contract")
ap.add_argument("-p", "--provider", required=False,
	help='RPC provider endpoint address (default is localhost port 8545)')
ap.add_argument("-u", "--account", required=False,
	help='User account (default is first account in eth.accounts)')
args = vars(ap.parse_args())

# assign provider name (defaults to http://127.0.0.1:8545)
if args["provider"] is not None:
    provider = args["provider"]
else:
    provider = "http://127.0.0.1:8545"

# define W3 Provider
w3 = Web3(Web3.HTTPProvider(provider))

# Use the first test account as the default account in the client if not specified
if args["account"] is not None:
    w3.eth.defaultAccount = args["account"]
else:
    w3.eth.defaultAccount = w3.eth.accounts[0]

def compile_source_file(file_path):
   with open(file_path, 'r') as f:
      source = f.read()
   return compile_source(source)

def instantiateContract(contract_name,contract_address):
    # Instantiate an existing contract. Requires original contract in order to generate ABI
    compiled_sol = compile_source_file(contract_name)
    
    # separate KV pair of id and interface
    contract_id, contract_interface = compiled_sol.popitem()
    
    # instantiate the contract
    contract = w3.eth.contract(address=contract_address, abi= contract_interface['abi'],)
    
    return contract

# ---------------------------------------------------------------------------------------

# Specific Contract Methods

def storeProof(proof):
    return True

def notarize(contract,document):
    tx_hash = contract.functions.notarize(document).transact()
    # print('Successfully Notarized:',document)
    # showGasCost(tx_hash)

def proofFor(contract,document):
    tx_hash = contract.functions.proofFor(document).call()
    print(tx_hash)
    return True

def checkDocument(contract,document):
    return(contract.functions.checkDocument(document).call())
    
def hasProof(proof):
    return True

# ---------------------------------------------------------------------------------------

def hashReadings(contract,filename):
    file = open(filename,'r')
    i = 0
    for line in file:
        notarize(contract,line)
        i += 1
    file.close()
    return i

def verifyReadings(contract,filename):
    file = open(filename,'r')
    i = 0
    fileInvalid = False
    for line in file:
        proof = checkDocument(contract,line)
        if proof == False:
            fileInvalid = True
            print('This reading is changed/not notarized:',line)
        i += 1
    file.close()
    return i,fileInvalid
    

def main():

    print('\nNotarization Demo')

    # assign contract name and address
    contract_name = args["contract"]
    contract_address = args["address"]

    print('\nInstantiating',contract_name,'from address',contract_address)

    # Instantiate the contract using contract_address
    contract = instantiateContract(contract_name,contract_address)

    # Begin test logic
    print('Using',contract_name,'contract.')

    exit = False

    while not(exit):
        option = input('\nDo you want to (n)otarize, (v)alidate or e(x)it: ')
        if option == 'n':
            filename = input('Enter collection of readings to notarize: ')
            num = hashReadings(contract,filename)
            print('Total of',num,'records notarized.')
        elif option == 'v':
            filename = input('Enter collection of readings to check notarization: ')
            num,invalid = verifyReadings(contract,filename)
            print(num,'records checked.')
            if invalid == True:
                print('Some data was invalid')
            else:
                print('All data is valid')
        elif option == 'x':
            exit = True
    
    print('Goodbye')
    
if __name__ == "__main__":
    main()