from etherscan.contracts import Contract
import json

with open('../../api_key.json', mode='r') as key_file:
    key = json.loads(key_file.read())['key']

address = '0xc5d105e63711398af9bbff092d4b6769c82f793d'

api = Contract(address=address, api_key=key)
abi = api.get_abi()
print(abi)
