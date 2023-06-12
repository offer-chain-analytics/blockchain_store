from web3 import Web3
from web3 import HTTPProvider
import web3
import json

with open('../config.json') as f:
    settings = json.load(f)

with open('../../build/contracts/AutoCar.json') as f:
    contract_info = json.load(f)

w3 = Web3(HTTPProvider('{host}:{port}'.format(
    host=settings['blockchain']['host'],
    port=settings['blockchain']['port']
)))

contract_address = web3.Web3.toChecksumAddress(settings['contract']['address'])

contract = w3.eth.contract(
    address=contract_address,
    abi=contract_info['abi'],
)


def unlock_account(account, password):
    return w3.geth.personal.unlock_account(account, password, 300)


def register_user(
    user_name,
    role,
    index=1
):
    # unlock_account(account, password)
    # TODO: create user

    contract.functions.registerUser(
        settings['users'][index]['address'],
        role,
        user_name
    ).transact({
        "from": settings['users'][index]['address']
    })

    return {
        "address": settings['users'][index]['address'],
        "password": settings['users'][index]['password']
    }


def add_stuff(
    user_login,
    user_password,
    location,
    vin_code,
    category,
    description,
    time
):
    # unlock_account(user_login, user_password)

    contract.functions.addStuff(
        location,
        vin_code,
        category,
        description,
        time
    ).transact({
        "from": user_login
    })


def modify_dict_stuff_to_object(stuff):
    return {
        "vincode": stuff[2],
        "address": stuff[1],
        "category": stuff[3],
        "description": stuff[4],
        "datetime": stuff[5]
    }


def get_all_stuffs_info(
    user_login,
    user_password,
    vin_code
):
    # unlock_account(user_login, user_password)

    stuff_list = contract.functions.getAllStuffsInfo(vin_code).call()

    return {
        "records" : list(map(modify_dict_stuff_to_object, stuff_list))
    }


def get_stuffs_info(
    user_login,
    user_password,
    vin_code,
    index
):
    # unlock_account(user_login, user_password)

    return modify_dict_stuff_to_object(contract.functions.getStuffInfo(vin_code, index).call())


if __name__ == '__main__':
    print(get_stuffs_info(settings['users'][1]['address'], "pass", "test_vin_code", 0))
