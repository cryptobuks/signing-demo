Veriteos Blockchain Signing Demo
(c) Veriteos, Inc. 2018 

Purpose

Notarizes/Checks Notarization for a file of readings using a deployed smart contract.
Demonstrates interacting with a smart contract on the permissioned Veriteos blockchain 

Dependencies:

verify.sol

Note: Deploy contract first using deploycontract script or other method.
This demo requires the deployed contract's address

Sample File
Use demo file: elemental.csv

Contract Methods:

Notarize: Stores the SHA256 for a given line of text.

Validate: Check to see if a given piece of text was previously hashed (ie; has this line changed from when it was last seen)

Usage: python NotarizeDemo.py -c verify.sol -a <contract address> [-p <provider endpoint>]
