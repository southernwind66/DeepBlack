import requests
from infura import web3
from config import *
import csv
import pandas as pd
import json
import time
from web3 import Web3

def getIPFSLink(id):
    try:
        response = requests.get("https://bitairt.io/api/photo/" + str(id))
        info = response.json()
        ipfs_link = info['image']
        return ipfs_link
    except:
        print("Failed to get DPB id " + str(id))
        print("Trying again in 5 sec")
        time.sleep(5)
        getIPFSLink(id)

def getAllLinks():
    d_address = Web3.toChecksumAddress(deepblack_address)
    dpb_contract = web3.eth.contract(address=d_address, abi=deepblack_abi)

    df = pd.DataFrame(columns=['ID', 'IPFS Link'])

    #Ignore the last 4 because it's 8001-8004
    for i in range(0, 3069):
        if i % 100 == 0:
            print(str(i) + " Deepblacks have been processed")

        id = dpb_contract.functions.tokenByIndex(i).call()
        link = getIPFSLink(id)
        df.append({'ID':id, 'IPFS Link':link}, ignore_index=True)
        time.sleep(0.2)
    
    df.to_csv("deepblackipfslinks.csv")
    return df

print(getAllLinks())
