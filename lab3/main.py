from web3 import Web3

# Подключение к узлу Ethereum (например, Infura)
w3 = Web3(Web3.HTTPProvider('https://sepolia.infura.io/v3/f4a17144fcd04034a0d486ecfdd611a5'))

# Адрес смарт-контракта и ABI (Application Binary Interface)
contract_address = '0x7781D705cBE27Cf38575E266B9128A870489F335'
contract_abi = [
    {
        "constant": True,
        "inputs": [],
        "name": "name",
        "outputs": [{"name": "", "type": "string"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {"name": "spender", "type": "address"},
            {"name": "tokens", "type": "uint256"}
        ],
        "name": "approve",
        "outputs": [{"name": "success", "type": "bool"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "totalSupply",
        "outputs": [{"name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {"name": "from", "type": "address"},
            {"name": "to", "type": "address"},
            {"name": "tokens", "type": "uint256"}
        ],
        "name": "transferFrom",
        "outputs": [{"name": "success", "type": "bool"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [{"name": "tokenOwner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [
            {"name": "tokenOwner", "type": "address"},
            {"name": "spender", "type": "address"}
        ],
        "name": "allowance",
        "outputs": [{"name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {"name": "to", "type": "address"},
            {"name": "tokens", "type": "uint256"}
        ],
        "name": "transfer",
        "outputs": [{"name": "success", "type": "bool"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "name": "from", "type": "address"},
            {"indexed": True, "name": "to", "type": "address"},
            {"indexed": False, "name": "tokens", "type": "uint256"}
        ],
        "name": "Transfer",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "name": "tokenOwner", "type": "address"},
            {"indexed": True, "name": "spender", "type": "address"},
            {"indexed": False, "name": "tokens", "type": "uint256"}
        ],
        "name": "Approval",
        "type": "event"
    }
]

# Создание экземпляра смарт-контракта
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Вызов функции (шаг 1)
def call_contract_function():
    account = '0xF936580B6c24FB9d7ef873785819a431B99d0FC0'
    private_key = '3b03a6d5ac1bc83b311e4a084e187e5b8ca55c8d30e7438410a8fb0c8f443c8d'
    nonce = w3.eth.get_transaction_count(account)

    # Подготовка данных для вызова функции transfer(address to, uint tokens)
    function_signature = contract.functions.transfer(
        '0x13AC5cac87866786007f2732eddDcD12f8DD9437',
        1
    ).build_transaction({
        'gas': 2000000,
        'gasPrice': w3.to_wei('100', 'gwei'),
        'nonce': nonce,
    })

    # Подписание транзакции
    signed_transaction = w3.eth.account.sign_transaction(function_signature, private_key)

    # Отправка транзакции
    transaction_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)

    # Ожидание подтверждения транзакции
    transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)

    return transaction_receipt

# Получение событий по контракту
def get_contract_events():
    events = contract.events.Transfer().get_logs(fromBlock='latest')
    return events

# Подписка на события
def subscribe_to_events():
    event_filter = contract.events.Transfer().create_filter(fromBlock='latest')
    while True:
        for event in event_filter.get_new_entries():
            print(event)

# Вызов функции (шаг 1)
transaction_receipt = call_contract_function()
print(f'Transaction Receipt: {transaction_receipt}')

# Получение событий по контракту
events = get_contract_events()
print(f'Contract Events: {events}')

# Подписка на события
subscribe_to_events()
