const Web3 = require('web3')
const fs = require('fs')
const path = require('path')

const settings = JSON.parse(fs.readFileSync(path.resolve(__dirname, '../config.json'), 'utf-8'));

const web3 = new Web3(new Web3.providers.HttpProvider(`${settings.blockchain.host}:${settings.blockchain.port}`))

const contractInfo = JSON.parse((fs.readFileSync(path.resolve(`../../build/contracts/AutoCar.json`), 'utf-8')))

var contract = new web3.eth.Contract(contractInfo.abi, {
	from: settings.users[1].address,
	data: contractInfo.bytecode
})

contract.options.address = settings.contract.address

const unlockUser = async (address, password) => {
    return await web3.eth.personal.unlockAccount(address, password, 1000)
}

export const registerUser = async (userName = '', role = 1) => {
    await unlockUser(settings.users[1].address, settings.users[1].password);

    return contract.methods.registerUser(
        settings.users[1].address,
        role,
        userName
    ).send()
}

export const addStuff = async (vincode, category, description, time) => {
    await unlockUser(settings.users[1].address, settings.users[1].password);

    return contract.methods.addStuff(vincode, category, description, time).send({
        from: settings.users[1].address,
        gas: 200000
    })
}

export default {
    registerUser,
    addStuff
}
